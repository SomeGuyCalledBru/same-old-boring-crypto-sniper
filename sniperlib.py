from time import time, sleep
from web3 import Web3
from common import log, w3, config, network_presets, FILENAME
import common
from threading import Thread
import json
from eth_account.account import Account
NULL = "0x0000000000000000000000000000000000000000"
class Sniper:
    def __init__(self, config, network, dex):
        self.pending_tx_count = 0
        self.config = config # Full configuration file, copied
        self.network = network # Network data EXCLUDING key name.
        self.dex = dex # DEx data EXCLUDING key name.
        self.WETH = network["weth"] # Ease of access
        self.factory = w3.eth.contract(address=self.network["main_contract"], abi=common.sniper_factory_abi) # The factory contract of the swapper.
        self.contract = w3.eth.contract(address=common.main_contract, abi=common.sniper_main_abi) # The contract of the swapper, deployed by the user.
        self.simulator = w3.eth.contract(address=self.network["hp_screener"], abi=common.simulator_abi) # The simulator contract, used to schedule buys and check for HP
        self.router = w3.eth.contract(address=common.network_presets["dexes"][self.config["network"]][self.config["dex"]]["router"], abi=common.uniswap_v2_router_abi) # UniV2 router
        self.trades = common.load_trades() # List of trades(buy&sell txs)
        self.simulations = {} # List of running(and not running) simulations
        self.chain_id = w3.eth.chain_id
        self.bootstrap_pending_trades() # The user can interrupt the bot while some transactions are pending. To not leave them hanging in later runs, this function's used.
        self.base_gas_price = 0
        self.pnl_thread_idle = False
        sleep(0.5)
        Thread(target=self.fetch_base_gas_price).start()
        Thread(target=self.pnl_logger).start()
        Thread(target=self.timeout_restorable).start()
        Thread(target=self.cleanup_thread).start()

    def deploy(self):
        tx = self.factory.encodeABI(fn_name="deploy", args=[])
        data = self.construct_tx_dict(1000000, Web3.toWei(5, 'gwei'), 0, True, self.factory.address)
        data["data"] = tx
        signed_tx = w3.eth.account.sign_transaction(data, self.config["privateKey"])
        return Web3.toHex(w3.eth.sendRawTransaction(signed_tx.rawTransaction))

    def set_params(self,AMOUNT_TO_USE, GAS_PARAMS):
        self.config["AMOUNT_TO_USE_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]] = AMOUNT_TO_USE
        self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]] = GAS_PARAMS
        self.set_config()

    def pnl(self, address, amount_in, amount_out):
        result = self.router.functions.getAmountsOut(amount_out, self.construct_path(address, NULL, "sell")).call()[-1]
        mul = round(result/amount_in, 5)
        return {
            "multiplier": mul,
            "percentage_string": f"{round((mul-1)*100, 4)}%",
            "if_sold_now": int(mul*amount_in)
        }

    def start(self, address, initiator="Unspecified"):
        # Lock in parameters
        amount_in = self.config["AMOUNT_TO_USE_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]]
        gas_params = self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]]
        Thread(target=self._start, args=(Web3.toChecksumAddress(address.replace(" ", "")), amount_in, gas_params, initiator)).start()

    def stop(self, address):
        del self.simulations[address]

    def _start(self, address, amount_in, gas_params, initiator):
        # meant to be called outside main thread.
        try:
            try:
                if self.simulations[address]["status"] == "Running": return
            except Exception:
                self.simulations[address] = {}
                pass
            try:
                if len([i for i in self.simulations if self.simulations[i]["status"] == "Running"]) >= 5:
                    return
            except KeyError:
                pass
            self.simulations[address]["status"] = "Running"
            self.simulations[address]["amount_in"] = amount_in
            self.simulations[address]["gas_price"] = gas_params[0]
            self.simulations[address]["gas_limit"] = gas_params[1]
            self.simulations[address]["adaptive_gas"] = gas_params[2]
            self.simulations[address]["initiator"] = initiator
            while True:
                start_time = time()
                result = self.simulate(address, amount_in)
                log.debug(f"Simulation took {time()-start_time} seconds.")
                if result or self.simulations[address]["status"] != "Running":
                    break
                sleep(self.config["intervalBetweenSimulationsMs"]/1000)
            if self.simulations[address]["status"] == "Running":
                self.swap(address, "buy", amount_in, gas_params, initiator=initiator)
                self.simulations[address]["status"] = "Succeeded!"
        except KeyError as e:
            # Means trade was deleted
            if address in str(e):
                pass
            else:
                log.error(f"Sim error: {e}")
                self.simulations[address]["status"] = "Errored"
                return
        except Exception as e:
            log.error(f"Sim error: {e}")
            self.simulations[address]["status"] = "Errored"
            return

    def simulate(self, address, amount_in):
        path = self.construct_path(address, NULL, "buy")
        calldata = self.simulator.encodeABI(fn_name='checkNow', args=[self.dex["router"], path, path[::-1], self.config["simulationTaxLimitPercent"]])
        try:
            w3.eth.call({"from": self.config["address"], "to": self.simulator.address, "data": calldata, "value": amount_in})
            return True
        except Exception as e:
            if 'execution reverted' in str(e).lower(): 
                log.warning(f"Exception in simulation, returning False: {e}{common.generate_kwargs(address=address)}")
                return False
            else:
                raise ValueError('Unknown error in simulation')

    def swap(self, address, side, amount_in, gas_params, initiator="Unspecified"):
        # amount_in: Amount input in WEI form if a buy, or in PERCENTAGE if a sell.
        # Load the encoder specified, just in case the DEX isn't uni v2 compatible.
        encoder = common.encoders[self.dex["encoder"]] 
        if side == "sell":
            perc = amount_in
            start_time = time()
            amount_in = int(self.get_token_balance(address)*perc/100) if perc < 100 else int(self.get_token_balance(address))
            log.debug(f"(SellSwap) amount in call completed in {round(time()-start_time, 2)} seconds")
        path = self.construct_path(address, NULL, side)
        # Encode calldata with the encoder function, specified for that DEX.
        start_time = time()
        calldata = encoder(int(amount_in*99/100) if side == "buy" else amount_in, path, common.main_contract, self.dex["router"])
        log.debug(f"(Encode) completed in {round(time()-start_time, 2)} seconds")
        # Standard transaction signing procedures
        start_time = time()
        tx_data = self.construct_tx_dict(gas_params[1], gas_params[0], amount_in if side == "buy" else 0, gas_params[2], self.contract.address)
        log.debug(f"(ConstructTx) completed in {round(time()-start_time, 2)} seconds")
        start_time = time()
        full_calldata = self.contract.encodeABI(fn_name="swap", args=[self.dex["router"], calldata, path[0], path[-1], side == "sell"])
        tx_data["data"] = full_calldata
        signed_transaction = w3.eth.account.sign_transaction(tx_data, self.config["privateKey"])
        log.debug(f"(BuildAndSign) completed in {round(time()-start_time, 2)} seconds")
        start_time = time()
        transaction_hash = Web3.toHex(w3.eth.sendRawTransaction(signed_transaction.rawTransaction))
        log.debug(f"(TxSubmit) completed in {round(time()-start_time, 2)} seconds")
        trade_result = {
            "address": address,
            "status": "Pending",
            "tx": transaction_hash,
            "amount_in": amount_in,
            "amount_out": 0,
            "gas_params": gas_params,
            "multiplier": 1, # Only for buys
            "percentage_string": "0%", # Only for buys
            "if_sold_now": amount_in, # Only for buys
            "balance_now": 0, # Only for buys
            "decimals": self.decs(address),
            "name": self.name(address),
            "initiator": initiator,
            "limit_orders": []
        }
        log.debug(trade_result)
        self.trades[side].append(trade_result)
        log.debug(f"(AddToTrades) completed")
        self.set_trades()
        self.update_trade(transaction_hash, side)
        return transaction_hash

    def construct_tx_dict(self, gas_limit, gas_price, value, adaptive_gas, to): 
        """Returns a full transaction data dictionary from config and parameters."""
        result = {
            "to": to,
            "chainId": self.chain_id,
            "nonce": w3.eth.get_transaction_count(self.config["address"], 'pending'),
            "from": self.config["address"],
            "gas": gas_limit,
            "value": value
        }
        if not self.network["eip1559"]:
            result["gasPrice"] = gas_price if not adaptive_gas else gas_price+self.base_gas_price
        else:
            if not adaptive_gas:
                result["maxFeePerGas"] = gas_price
            else:
                result["maxFeePerGas"] = gas_price+self.base_gas_price
            result["maxPriorityFeePerGas"] = gas_price
        return result

    def construct_path(self, address, route, side):
        if route == "0x0000000000000000000000000000000000000000":
            # Make the path direct if the buying route is the null address.
            if side == "buy":
                path = [self.WETH, address]
            else:
                path = [address, self.WETH]
        else:
            # If not, insert the path in the middle for the swap to work.
            if side == "buy":
                path = [self.WETH, route, address]
            else:
                path = [address, route, self.WETH]
        return path

    def restore_trade(self, address):
        found = False
        copy = self.trades["restorable"]["buy"]
        # Check if the address exists outside the restorable list.
        for i, trade in enumerate(self.trades["buy"]):
            if trade["address"] == address:
                found = True
                break
        for i, restorable in enumerate(copy):
            if restorable["address"] == address:
                self.trades["buy"].append({key: restorable[key] for key in restorable if key != "time"})
                self.trades["restorable"]["buy"][i]["status"] = "Halted"
                found = True
        self.trades["restorable"]["buy"] = [i for i in self.trades["restorable"]["buy"] if i["status"] != "Halted"]
        copy = self.trades["restorable"]["sell"]
        for i, restorable in enumerate(copy):
            if restorable["address"] == address:
                self.trades["sell"].append({key: restorable[key] for key in restorable if key != "time"})
                self.trades["restorable"]["sell"][i]["status"] = "Halted"
        self.trades["restorable"]["sell"] = [i for i in self.trades["restorable"]["sell"] if i["status"] != "Halted"]
        log.debug(f"{found}")
        if not found:
            trade_result = {
                "address": address,
                "status": "Successful",
                "tx": "0x0000000000000000000000000000000000000000000000000000000000000000",
                "amount_in": 0,
                "amount_out": 0,
                "gas_params": [0, 0, False],
                "multiplier": 1, # Only for buys
                "percentage_string": "0%", # Only for buys
                "if_sold_now": 0, # Only for buys
                "balance_now": 0, # Only for buys
                "decimals": self.decs(address),
                "name": self.name(address),
                "initiator": "blank",
                "limit_orders": []
            }
            self.trades["buy"].append(trade_result)
        self.set_trades()
    
    def delete_trade(self, side, index):
        # These comments may be silly. Thank Copilot-I'm making it write my code.
        # Back up trade only if tx is not 0x0000000000000000000000000000000000000000000000000000000000000000(blank).
        if self.trades[side][index]["tx"] != "0x0000000000000000000000000000000000000000000000000000000000000000":
            trade_result  ={**self.trades[side][index], **{'time': time()}}
            self.trades["restorable"][side].append(trade_result)
        # Set status to "Halted"
        self.trades[side][index]["status"] = "Halted"
        self.set_trades()

    def fetch_base_gas_price(self): 
        while True:
            try:
                result = w3.eth.get_block('latest').baseFeePerGas if self.network["eip1559"] else w3.eth.gas_price
                self.base_gas_price = result
                log.info(f"Updated base gas, result: {result}")
            except Exception as e:
                log.warning(f"Failed to update base gas, error: {e}")
            sleep(5)

    def timeout_restorable(self):
        # Delete restorable trades if it's been 7 days since the last time it was made.
        while True:
            for side in ["buy", "sell"]:
                for i, res in enumerate(self.trades["restorable"][side]):
                    if time()-res["time"] > 86400*7:
                        self.trades["restorable"][side][i]["status"] = "Halted"
                self.trades["restorable"][side] = [i for i in self.trades["restorable"][side] if i["status"] != "Halted"]
                self.set_trades()
            sleep(30)
            
    def get_token_balance(self, address): """Returns the token balance in the contract."""; return w3.eth.contract(address=address, abi=common.erc_abi).functions.balanceOf(common.main_contract).call()
    def decs(self, address): """Returns the token decimals."""; return w3.eth.contract(address=address, abi=common.erc_abi).functions.decimals().call()
    def name(self, address): """Returns the token name."""; return w3.eth.contract(address=address, abi=common.erc_abi).functions.name().call()
    def bootstrap_pending_trades(self):
        for i in self.trades["buy"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "buy")
        for i in self.trades["sell"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "sell")

    def pnl_logger(self):
        while True:
            self.pnl_thread_idle = False
            for i in range(len(self.trades["buy"])):
                if self.trades["buy"][i]["status"] == "Successful" and self.trades["buy"][i]["amount_in"] > 0: # last condition is to skip restored tx
                    try:
                        log.info(f"Getting PNL&balance for {self.trades['buy'][i]}")
                        result = self.pnl(self.trades["buy"][i]["address"], self.trades["buy"][i]["amount_in"], self.trades["buy"][i]["amount_out"])
                        log.info(f"PNL log: {result}, address: {self.trades['buy'][i]['address']}, index: {i}")
                        self.trades["buy"][i]["multiplier"] = result["multiplier"]
                        self.trades["buy"][i]["percentage_string"] = result["percentage_string"]
                        self.trades["buy"][i]["if_sold_now"] = result["if_sold_now"]
                        self.trades["buy"][i]["balance_now"] = self.get_token_balance(self.trades["buy"][i]["address"])

                        log.info("Checking limit orders")
                        for limit_index, limit_order in enumerate(self.trades["buy"][i]["limit_orders"]):
                            if limit_order["trigger"] > 1 and result["multiplier"] >= limit_order["trigger"]:
                                log.info(f"TP: {limit_order} hit, sending tx")
                                self.swap(self.trades['buy'][i]['address'], "sell", limit_order["percentage"], self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]], initiator="limit sell(TP)")
                                self.delete_limit(i, limit_index)
                            elif limit_order["trigger"] < 1 and result["multiplier"] <= limit_order["trigger"]:
                                log.info(f"SL: {limit_order} hit, sending tx")
                                self.swap(self.trades['buy'][i]['address'], "sell", limit_order["percentage"], self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]], initiator="limit sell(SL)")
                                self.delete_limit(i, limit_index)
                        self.set_trades()
                    except Exception as e:
                        log.error(f"PNL log error: {e}")
                    sleep(2)
                elif self.trades["buy"][i]["status"] == "Successful" and self.trades["buy"][i]["amount_in"] == 0:
                    log.info(f"{self.trades['buy'][i]} is a restored trade, skipping")
                    self.trades["buy"][i]["balance_now"] = self.get_token_balance(self.trades["buy"][i]["address"])
                    self.set_trades()
                    sleep(1)
            # Allow time for cleanup threads to run
            self.pnl_thread_idle = True
            sleep(0.1)

    def delete_limit(self, trade_index, limit_index): 
        log.info(f"Deleting limit order, data: {self.trades['buy'][trade_index]['limit_orders'][limit_index]}")
        del self.trades["buy"][trade_index]["limit_orders"][limit_index]
        self.set_trades()

    def set_limit(self, trade_index, multiplier, percentage): 
        self.trades["buy"][trade_index]["limit_orders"].append({'trigger': multiplier, 'percentage': percentage})
        log.info(f"Set limit: {multiplier}, {percentage}")
        self.set_trades()
        
    def update_trade(self, tx_hash, side): Thread(target=self._update_trade, args=(tx_hash, side)).start()
    def _update_trade(self, tx_hash, side):
        self.pending_tx_count += 1
        try:
            if side == "buy":
                for i in range(len(self.trades["buy"])):
                    # Get the matching trade by iterating through it
                    if self.trades["buy"][i]["tx"] == tx_hash:
                        address = self.trades["buy"][i]["address"]
                        token_contract = w3.eth.contract(address=address, abi=common.erc_abi)
                        # Wait for the transaction receipt. We're interested in the status and the logs.
                        log.info(f"Waiting for transaction receipt: {tx_hash}")
                        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                        log.info(f"Transaction receipt received: {tx_receipt}")
                        # Report a failed transaction.
                        if not tx_receipt.status:
                            log.error(f"Transaction failed: {tx_receipt}")
                            self.trades["buy"][i]["status"] = "Failed"
                            self.set_trades()
                            self.pending_tx_count -= 1
                            return
                        # If we succeeded, we can move on.
                        logs = token_contract.events.Transfer().processReceipt(tx_receipt)
                        log.debug(f"Transaction logs: {logs}, hash: {tx_hash}")
                        totalOutput = 0
                        for txlog in logs:
                            # If a log:
                            # - is emitted from the target token
                            # - is a transfer with the destination as the contract wallet
                            # then we can say it's a valid output.
                            if Web3.toChecksumAddress(txlog.args.to) == self.contract.address and Web3.toChecksumAddress(address) == txlog.address:
                                log.debug(f"Valid output: {txlog}")
                                totalOutput += txlog.args.value
                        # Update the necessary values and return
                        self.trades["buy"][i]["amount_out"] = totalOutput
                        self.trades["buy"][i]["status"] = "Successful"
                        self.set_trades()
                        log.info(f"Trade updated: {self.trades['buy'][i]}")
                        self.pending_tx_count -= 1
                        return 
            elif side == "sell":
                for i in range(len(self.trades["sell"])):
                    # Get the matching trade by iterating through it
                    if self.trades["sell"][i]["tx"] == tx_hash:
                        WETH_contract = w3.eth.contract(address=self.WETH, abi=common.erc_abi)
                        # Wait for the transaction receipt. We're interested in the status and the logs.
                        log.info(f"Waiting for transaction receipt: {tx_hash}")
                        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                        log.info(f"Transaction receipt received: {tx_receipt}")
                        # Report a failed transaction.
                        if not tx_receipt.status:
                            log.error(f"Transaction failed: {tx_receipt}")
                            self.trades["sell"][i]["status"] = "Failed"
                            self.set_trades()
                            self.pending_tx_count -= 1
                            return
                        # If we succeeded, we can move on.
                        logs = WETH_contract.events.Transfer().processReceipt(tx_receipt)
                        log.debug(f"Transaction logs: {logs}, hash: {tx_hash}")
                        totalOutput = 0
                        for txlog in logs:
                            # If a log:
                            # - is emitted from the target token
                            # - is a transfer with the destination as the contract wallet
                            # then we can say it's a valid output.
                            if Web3.toChecksumAddress(txlog.args.to) == self.contract.address and self.WETH == txlog.address:
                                log.debug(f"Valid output: {txlog}")
                                totalOutput += txlog.args.value
                        # Update the necessary values and return
                        self.trades["sell"][i]["amount_out"] = totalOutput
                        self.trades["sell"][i]["status"] = "Successful"
                        self.set_trades()
                        log.info(f"Trade updated: {self.trades['sell'][i]}")
                        self.pending_tx_count -= 1
                        return 
        except Exception as e:
            log.error(f"Error updating trade: {e}")
            self.pending_tx_count -= 1
            return

    def set_trades(self): 
        with open(FILENAME, "w") as f: 
            json.dump(self.trades, f, indent=4)
        log.info(f"Trades updated")
    
    def set_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def cleanup(self):
        # Remove all trades that are finished.
        for side in ["buy", "sell"]:
            self.trades[side] = [trade for trade in self.trades[side] if trade["status"] != "Halted"]
        self.set_trades()

    def cleanup_thread(self):
        while True:
            # Wait for the PNL and tx updater threads to finish.
            # This is necessary because you can end up with index shifts if you don't, and that will be bad. Like, really bad.
            if self.pending_tx_count == 0 and self.pnl_thread_idle and len([i for i in self.trades["buy"] if i["status"] == "Pending"]) == 0 and len([i for i in self.trades["sell"] if i["status"] == "Pending"]) == 0:                 
                self.cleanup()
                # Prevent repeated cleanup.
                sleep(1)
            sleep(0.01)

# Had to move out due to circular imports
sniper = Sniper(config=config, network=network_presets["networks"][config["network"]], dex=network_presets["dexes"][config["network"]][config["dex"]])