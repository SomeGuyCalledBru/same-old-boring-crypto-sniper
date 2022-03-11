import random
from time import time, sleep
from web3 import Web3
import common
from threading import Thread
import json
from requests import get
NULL = "0x0000000000000000000000000000000000000000"
class Sniper:
    def __init__(self, config, network, dex, start_threads=True):
        self.pending_tx_count = 0
        self.config = config # Full configuration file, copied
        self.network = network # Network data EXCLUDING key name.
        self.dex = dex # DEx data EXCLUDING key name.
        self.WETH = network["weth"] # Ease of access
        self.factory = common.w3.eth.contract(address=self.network["main_contract"], abi=common.sniper_factory_abi) # The factory contract of the swapper.
        self.contract = common.w3.eth.contract(address=common.main_contract, abi=common.sniper_main_abi) # The contract of the swapper, deployed by the user.
        self.simulator = common.w3.eth.contract(address=self.network["hp_screener"], abi=common.simulator_abi) # The simulator contract, used to schedule buys and check for HP
        self.router = common.w3.eth.contract(address=common.network_presets["dexes"][self.config["network"]][self.config["dex"]]["router"], abi=common.uniswap_v2_router_abi) # UniV2 router
        self.trade_init()
        # It's actually snipes not simulations but I'm too lazy to change the name
        self.simulations = {} # List of running(and not running) snipes
        self.chain_id = self.network["chainId"]
        self.bootstrap_pending_trades() # The user can interrupt the bot while some transactions are pending. To not leave them hanging in later runs, this function's used.
        self.base_gas_price = 0
        self.ticker_price = get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.network['cgApi']}&vs_currencies=usd").json()[self.network['cgApi']]['usd']
        self.paused = False
        try:
            self.txpool = common.w3.geth.txpool.content()
            self.txpool_support = True
        except Exception as e:
            self.txpool = {}
            self.txpool_support = False
        common.log.info(f"Ticker price: {self.ticker_price}")
        sleep(0.5)
        if start_threads:
            Thread(target=self.fetch_base_gas_price).start()
            Thread(target=self.timeout_restorable).start()
            Thread(target=self.cleanup_thread).start()
            Thread(target=self.ticker_price_getter).start()
            Thread(target=self.execute_limit_orders).start()
            Thread(target=self.update_txpool).start()

    def deploy(self):
        tx = self.factory.encodeABI(fn_name="deploy", args=[])
        data = self.construct_tx_dict(1000000, Web3.toWei(5, 'gwei'), 0, True, self.factory.address)
        data["data"] = tx
        signed_tx = common.w3.eth.account.sign_transaction(data, self.config["privateKey"])
        return Web3.toHex(common.w3.eth.sendRawTransaction(signed_tx.rawTransaction))

    def set_params(self, AMOUNT_TO_USE, GAS_PARAMS, AMOUNT_UNIT):
        self.config["AMOUNT_TO_USE_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]] = AMOUNT_TO_USE
        self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]] = GAS_PARAMS
        self.config["amountUnit"][self.config["network"]] = AMOUNT_UNIT
        self.set_config()

    def pnl(self, address, amount_in, amount_out):
        result = self.router.functions.getAmountsOut(amount_out, self.construct_path(address, NULL, "sell")).call()[-1]
        mul = round(result/amount_in, 5)
        return {
            "multiplier": mul,
            "percentage_string": f"{round((mul-1)*100, 4)}%",
            "if_sold_now": int((mul-1)*amount_in),
        }                

    def address_only_pnl(self, address):
        amount_in = 0
        amount_out = 0
        decimals = 0
        for trade in self.trades["buy"]:
            if trade["address"] == address and trade["status"] == "Successful":
                decimals = trade["decimals"]
                amount_in += trade["amount_in"]
                amount_out += trade["amount_out"]
        if not amount_in or not amount_out:
            return None
        return self.pnl(address, amount_in, amount_out)

    def start_snipe(self, address, type, amount=None, amount_unit=None, initiator="Unspecified", rules=[]):
        # Fall back to the configured amount if none is specified
        if not amount:
            amount = self.config["AMOUNT_TO_USE_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]]
        # Fall back to the configured amount unit if none is specified
        if not amount_unit:
            amount_unit = self.config["amountUnit"][self.config["network"]]
        # Unique identifier for the snipe
        # This identifier is kept for the lifetime of the snipe
        # It is used to stop the snipe and to prevent array index errors
        identifier = str(random.randint(0, 10**18))
        # Make sure the identifier is not already in use
        while identifier in self.simulations:
            identifier = str(random.randint(0, 10**18))
        Thread(target=self._start, args=(Web3.toChecksumAddress(address.replace(" ", "")), amount, amount_unit, type, initiator, identifier, rules)).start()

    def stop_standard_snipe(self, ident):
        del self.simulations[ident]

    def _start(self, address, amount, amount_unit, type, initiator, identifier, rules=[]):
        self.simulations[identifier] = {
            "address": address,
            "amount": amount,
            "amount_unit": amount_unit,
            "initiator": initiator,
            "type": type
        }
        if type == "stdSnipe":
            try:
                amount_for_simulation = self.calculate_amount(address, "buy", amount, amount_unit)
                initial_iteration = True # Speed up the first iteration
                while True:
                    if initial_iteration:
                        initial_iteration = False
                    else:
                        sleep(self.config["intervalBetweenSimulationsMs"]/1000)
                    result = self.simulate(address, amount_for_simulation)
                    if result:
                        break
                    # Leave early if the user has stopped the snipe
                    if identifier not in self.simulations:
                        return
                self.swap(address, "buy", amount, amount_unit, initiator=initiator)
                del self.simulations[identifier]
                return 
            except Exception as e:
                common.log.error(f"Error while simulating {address}: {e}")
                del self.simulations[identifier]
                return
        elif type == "memSnipe":
            while True:
                # Leave early if the user has stopped the snipe
                if identifier not in self.simulations:
                    return
                # Iterate over the txpool
                for key, value in self.txpool.pending.items():
                    for nonce, nonce_value in value.items():
                        if self.test_transaction(nonce_value, rules):
                            # If the transaction is valid, send it
                            # Make sure the transaction is right after the target by using the same gas price
                            self.swap(address, "buy", amount, amount_unit, initiator=initiator, gas_price=int(nonce_value["gasPrice"], 16))
                            del self.simulations[identifier]
                            return
                sleep(0.01)

    def test_transaction(self, tx, rules):
        from_matching = [None for i in range(len(rules))]
        to_matching = [None for i in range(len(rules))]
        methodID_matching = [None for i in range(len(rules))]
        input_matching = [None for i in range(len(rules))]
        for index, rule in enumerate(rules):
            if rule["methodID"] != "0x00000000" and tx["input"][:10] == rule["methodID"]:
                methodID_matching[index] = True
            elif rule["methodID"] == "0x00000000":
                methodID_matching[index] = None
            elif rule["methodID"] != "0x00000000" and tx["input"][:10] != rule["methodID"]:
                methodID_matching[index] = False
            if rule["from"] != "0x0000000000000000000000000000000000000000" and tx["from"].lower() == rule["from"].lower():
                from_matching[index] = True
            elif rule["from"] == "0x0000000000000000000000000000000000000000":
                from_matching[index] = None
            elif rule["from"] != "0x0000000000000000000000000000000000000000" and tx["from"].lower() != rule["from"].lower():
                from_matching[index] = False
            if rule["to"] != "0x0000000000000000000000000000000000000000" and tx["to"].lower() == rule["to"].lower():
                to_matching[index] = True
            elif rule["to"] == "0x0000000000000000000000000000000000000000":
                to_matching[index] = None
            elif rule["to"] != "0x0000000000000000000000000000000000000000" and tx["to"].lower() != rule["to"].lower():
                to_matching[index] = False
            try:
                if rule["input"] != "" and rule["input"] in tx["input"].lower():
                    input_matching[index] = True
                elif rule["input"] == "":
                    input_matching[index] = None
                elif rule["input"] != "" and rule["input"] not in tx["input"].lower():
                    input_matching[index] = False
            except KeyError:
                # Handle the user passing nothing for the input
                input_matching[index] = None
        common.log.info(f"{from_matching} {to_matching} {methodID_matching} {input_matching}")
        return not(False in from_matching or False in to_matching or False in methodID_matching or False in input_matching)         

    def simulate(self, address, amount_in):
        path = self.construct_path(address, NULL, "buy")
        calldata = self.simulator.encodeABI(fn_name='checkNow', args=[self.dex["router"], path, path[::-1], self.config["simulationTaxLimitPercent"]])
        try:
            # TODO: Test balance override on all nodes
            common.w3.eth.call({"from": self.config["address"], "to": self.simulator.address, "data": calldata, "value": amount_in, "gasPrice": 0}, "pending", {self.config["address"]: {"balance": hex(2**256-1)}})
            return True
        except Exception as e:
            if 'execution reverted' in str(e).lower(): 
                common.log.warning(f"Exception in simulation, returning False: {e}{common.generate_kwargs(address=address)}")
                return False
            else:
                raise ValueError('Unknown error in simulation: ' + str(e))

    def get_price(self, address, is_usd, decimals):
        result = self.router.functions.getAmountsOut(Web3.toWei(0.01, 'ether'), self.construct_path(address, NULL, "buy")).call()[-1]
        price_in_native_token = Web3.toWei(0.01, 'ether')/result
        if is_usd:
            return (price_in_native_token*self.ticker_price)/10**(18-decimals)
        else:
            return price_in_native_token/10**(18-decimals)

    def get_output(self, address, side=None, amount_in=None):
        if not side:
            side = "buy"
        if not amount_in:
            amount_in = Web3.toWei(0.01, 'ether')
        return self.router.functions.getAmountsOut(amount_in, self.construct_path(address, NULL, side)).call()[-1]

    def swap(self, address, side, amount, amount_unit, initiator="Unspecified", absolute_amount_if_sell=False, gas_price=None):
        amount_in = self.calculate_amount(address, side, amount, amount_unit)   
        common.log.info(amount_in)
        gas_params = self.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][self.config["network"]]
        if gas_price:
            gas_params[0] = gas_price
            gas_params[2] = False
        encoder = common.encoders[self.dex["encoder"]] 
        path = self.construct_path(address, NULL, side)
        # Encode calldata with the encoder function, specified for that DEX.
        start_time = time()
        calldata = encoder(int(amount_in*99/100) if side == "buy" else amount_in, path, common.main_contract, self.dex["router"])
        common.log.debug(f"(Encode) completed in {round(time()-start_time, 2)} seconds")
        # Standard transaction signing procedures
        start_time = time()
        tx_data = self.construct_tx_dict(gas_params[1], gas_params[0], amount_in if side == "buy" else 0, gas_params[2], self.contract.address)
        common.log.debug(f"(ConstructTx) completed in {round(time()-start_time, 2)} seconds")
        start_time = time()
        full_calldata = self.contract.encodeABI(fn_name="swap", args=[self.dex["router"], calldata, path[0], path[-1], side == "sell"])
        common.log.debug(f"(EncodeABI) completed in {round(time()-start_time, 2)} seconds")
        start_time = time()
        tx_data["data"] = full_calldata
        signed_transaction = common.w3.eth.account.sign_transaction(tx_data, self.config["privateKey"])
        common.log.debug(f"(BuildAndSign) completed in {round(time()-start_time, 2)} seconds")
        start_time = time()
        transaction_hash = Web3.toHex(common.w3.eth.sendRawTransaction(signed_transaction.rawTransaction))
        common.log.debug(f"(TxSubmit) completed in {round(time()-start_time, 2)} seconds")
        trade_result = {
            "address": address,
            "status": "Pending",
            "tx": transaction_hash,
            "amount_in": amount_in,
            "amount": amount,
            "amount_unit": amount_unit,
            "amount_out": 0,
            "gas_params": gas_params,
            "decimals": self.decs(address),
            "name": self.name(address),
            "initiator": initiator,
            "limit_orders": [] # Never actually used, but needed to not break the frontend
        }
        if side == "buy":
            trade_result["multiplier"] = 1
            trade_result["percentage_string"] = "0%"
            trade_result["if_sold_now"] = amount_in
            trade_result["balance_now"] = 0
        common.log.debug(f"[{side.upper()}] {trade_result}")
        self.trades[side].append(trade_result)
        common.log.debug(f"(AddToTrades) completed")
        self.set_trades()
        self.update_trade(transaction_hash, side)
        return transaction_hash

    def update_txpool(self):
        while True:
            if len([i for i in self.simulations if self.simulations[i]["type"] == "memSnipe"]) > 0:
                try:
                    self.txpool = common.w3.geth.txpool.content()
                except Exception as e:
                    common.log.error(f"Error in update_txpool: {e}")
                    sleep(10)
            sleep(0.25)
            
    def construct_tx_dict(self, gas_limit, gas_price, value, adaptive_gas, to): 
        """Returns a full transaction data dictionary from config and parameters."""
        result = {
            "to": to,
            "chainId": self.chain_id,
            "nonce": common.w3.eth.get_transaction_count(self.config["address"], 'pending'),
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

    def execute_limit_orders(self):
        # Iterate through all limit orders and execute them if conditions are met.
        while True:
            for i, order in enumerate(self.trades["limits"]):
                if not order["executed"]:
                    if order["priceUnit"] == "percentage":
                        if order["type"] == "tp":
                            price_met = order["outputAtTimeOfCreation"] / self.get_output(order["address"]) >= order["price"]
                        elif order["type"] == "sl":
                            price_met = order["outputAtTimeOfCreation"] / self.get_output(order["address"]) <= order["price"]
                    else:
                        if order["type"] == "tp":
                            price_met = self.get_price(order["address"], order["priceUnit"] == "usd", order["decimals"]) >= order["price"]
                        elif order["type"] == "sl":
                            price_met = self.get_price(order["address"], order["priceUnit"] == "usd", order["decimals"]) <= order["price"]
                    if price_met:
                        self.swap(order["address"], order["side"], order["amount"], order["amountUnit"], initiator=f"limit {order['side']}", absolute_amount_if_sell=True)
                        self.trades["limits"][i]["executed"] = True
                sleep(1)
            # Clean up 
            self.trades["limits"] = [order for order in self.trades["limits"] if not order["executed"]]
            sleep(0.05)

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
        common.log.debug(f"{found}")
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
                result = common.w3.eth.get_block('latest').baseFeePerGas if self.network["eip1559"] else common.w3.eth.gas_price
                self.base_gas_price = result
                common.log.info(f"Updated base gas, result: {result}")
            except Exception as e:
                common.log.warning(f"Failed to update base gas, error: {e}")
            sleep(5)

    def ticker_price_getter(self):
        while True:
            try:
                self.ticker_price = get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.network['cgApi']}&vs_currencies=usd").json()[self.network['cgApi']]['usd']
                common.log.info(f"Updated ticker price, result: {self.ticker_price}")
            except Exception as e:
                common.log.warning(f"Failed to update ticker price, error: {e}")
            sleep(60)

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
            
    def get_token_balance(self, address): """Returns the token balance in the contract."""; return common.w3.eth.contract(address=address, abi=common.erc_abi).functions.balanceOf(common.main_contract).call()
    def decs(self, address): """Returns the token decimals."""; return common.w3.eth.contract(address=address, abi=common.erc_abi).functions.decimals().call()
    def name(self, address): """Returns the token name."""; return common.w3.eth.contract(address=address, abi=common.erc_abi).functions.name().call()
    def bootstrap_pending_trades(self):
        for i in self.trades["buy"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "buy")
        for i in self.trades["sell"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "sell")

    def set_limit(self, address, side, type, amount, amount_unit, price, price_unit): 
        limit_result = {
            "address": address,
            "side": side,
            "type": type,
            "price": price,
            # nativeToken/usd/percentage
            "priceUnit": price_unit,
            "amount": amount,
            # nativeToken/usd/percentage
            "amountUnit": amount_unit,
            "outputAtTimeOfCreation": self.get_output(address),
            "executed": False,
            "decimals": self.decs(address),
            "name": self.name(address)
        }
        if side == "buy" and amount_unit == "nativeToken":
            limit_result["amount"] = int(limit_result["amount"]*10**18)
        elif side == "sell" and amount_unit == "nativeToken":
            limit_result["amount"] = int(limit_result["amount"]*10**limit_result["decimals"])
        self.trades["limits"].append(limit_result)
        self.set_trades()

    def set_market(self, address, side, amount, amount_unit):
        self.swap(address, side, amount, amount_unit, initiator=f"market {side}", absolute_amount_if_sell=True)

    def calculate_amount(self, address, side, amount, amount_unit, decs=None):
        if side == "buy":
            if amount_unit == "percentage":
                result = common.w3.eth.get_balance(self.config["address"])
                amount = int(result*amount) // 100 if amount < 99 else result
            elif amount_unit == "nativeToken":
                amount = Web3.toWei(amount, "ether")
            elif amount_unit == "usd":
                amount = Web3.toWei(amount/self.ticker_price, "ether")
        elif side == "sell":
            if decs == None:
                # What is speed anyway?
                decs = self.decs(address)
            common.log.info(f"{address} decimals: {decs}")
            if amount_unit == "percentage":
                result = self.get_token_balance(address)
                common.log.info(f"{address} balance: {result}(percentage)")
                # Handle float (un)precision
                amount = int(result * amount) // 100 if amount < 99 else result
            elif amount_unit == "nativeToken":
                amount = int(amount*10**decs)
            elif amount_unit == "usd":
                result = self.get_price(address, True, decs)
                common.log.info(f"{address} price: {result}(usd)")
                amount = int(amount/(result/10**decs))
        return amount

    def delete_limit(self, index):
        self.trades["limits"][index]["executed"] = True

    def update_trade(self, tx_hash, side): Thread(target=self._update_trade, args=(tx_hash, side)).start()
    def _update_trade(self, tx_hash, side):
        self.pending_tx_count += 1
        try:
            if side == "buy":
                for i in range(len(self.trades["buy"])):
                    # Get the matching trade by iterating through it
                    if self.trades["buy"][i]["tx"] == tx_hash:
                        address = self.trades["buy"][i]["address"]
                        token_contract = common.w3.eth.contract(address=address, abi=common.erc_abi)
                        # Wait for the transaction receipt. We're interested in the status and the logs.
                        common.log.info(f"Waiting for transaction receipt: {tx_hash}")
                        tx_receipt = common.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                        common.log.info(f"Transaction receipt received: {tx_receipt}")
                        # Report a failed transaction.
                        if not tx_receipt.status:
                            common.log.error(f"Transaction failed: {tx_receipt}")
                            self.trades["buy"][i]["status"] = "Failed"
                            self.set_trades()
                            self.pending_tx_count -= 1
                            return
                        # If we succeeded, we can move on.
                        logs = token_contract.events.Transfer().processReceipt(tx_receipt)
                        common.log.debug(f"Transaction logs: {logs}, hash: {tx_hash}")
                        totalOutput = 0
                        for txlog in logs:
                            # If a log:
                            # - is emitted from the target token
                            # - is a transfer with the destination as the contract wallet
                            # then we can say it's a valid output.
                            if Web3.toChecksumAddress(txlog.args.to) == self.contract.address and Web3.toChecksumAddress(address) == txlog.address:
                                common.log.debug(f"Valid output: {txlog}")
                                totalOutput += txlog.args.value
                        # Update the necessary values and return
                        self.trades["buy"][i]["amount_out"] = totalOutput
                        self.trades["buy"][i]["status"] = "Successful"
                        self.set_trades()
                        common.log.info(f"Trade updated: {self.trades['buy'][i]}")
                        self.pending_tx_count -= 1
                        return 
            elif side == "sell":
                for i in range(len(self.trades["sell"])):
                    # Get the matching trade by iterating through it
                    if self.trades["sell"][i]["tx"] == tx_hash:
                        WETH_contract = common.w3.eth.contract(address=self.WETH, abi=common.erc_abi)
                        # Wait for the transaction receipt. We're interested in the status and the logs.
                        common.log.info(f"Waiting for transaction receipt: {tx_hash}")
                        tx_receipt = common.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                        common.log.info(f"Transaction receipt received: {tx_receipt}")
                        # Report a failed transaction.
                        if not tx_receipt.status:
                            common.log.error(f"Transaction failed: {tx_receipt}")
                            self.trades["sell"][i]["status"] = "Failed"
                            self.set_trades()
                            self.pending_tx_count -= 1
                            return
                        # If we succeeded, we can move on.
                        logs = WETH_contract.events.Transfer().processReceipt(tx_receipt)
                        common.log.debug(f"Transaction logs: {logs}, hash: {tx_hash}")
                        totalOutput = 0
                        for txlog in logs:
                            # If a log:
                            # - is emitted from the target token
                            # - is a transfer with the destination as the contract wallet
                            # then we can say it's a valid output.
                            if Web3.toChecksumAddress(txlog.args.to) == self.contract.address and self.WETH == txlog.address:
                                common.log.debug(f"Valid output: {txlog}")
                                totalOutput += txlog.args.value
                        # Update the necessary values and return
                        self.trades["sell"][i]["amount_out"] = totalOutput
                        self.trades["sell"][i]["status"] = "Successful"
                        self.set_trades()
                        common.log.info(f"Trade updated: {self.trades['sell'][i]}")
                        self.pending_tx_count -= 1
                        return 
        except Exception as e:
            common.log.error(f"Error updating trade: {e}")
            self.pending_tx_count -= 1
            return

    def set_trades(self): 
        if not self.paused:
            with open(f"trades-{self.config['network']}-{self.config['dex']}.json", "w") as f: 
                json.dump(self.trades, f, indent=4)
            common.log.info(f"Trades updated")
        else:
            common.log.warning(f"Changes are pending, not applying trades")
    
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
            if self.pending_tx_count == 0 and len([i for i in self.trades["buy"] if i["status"] == "Pending"]) == 0 and len([i for i in self.trades["sell"] if i["status"] == "Pending"]) == 0:                 
                self.cleanup()
                # Prevent repeated cleanup.
                sleep(1)
            sleep(0.01)

    def trade_init(self):
        try:
            with open(f"trades-{self.config['network']}-{self.config['dex']}.json", "r") as f: 
                self.trades = json.load(f)
                return True
        except Exception as e:
            with open(f"trades-{self.config['network']}-{self.config['dex']}.json", "w+") as f:
                json.dump({"limits": [], "buy": [], "sell": [], "restorable": {"buy": [], "sell": []}}, f)
        with open(f"trades-{self.config['network']}-{self.config['dex']}.json", "r") as f: 
            self.trades = json.load(f)
            return True

    def reinit(self, network, dex):
        self.paused = True  
        self.config["network"] = network
        self.config["dex"] = dex
        common.reinit(common.network_presets["networks"][network], common.network_presets["dexes"][network][dex], self.config)
        self.__init__(self.config, common.network_presets["networks"][common.config["network"]], common.network_presets["dexes"][common.config["network"]][common.config["dex"]], start_threads=False)
        self.set_config()
        self.paused = False

# Had to move out due to circular imports
sniper = Sniper(config=common.config, network=common.network_presets["networks"][common.config["network"]], dex=common.network_presets["dexes"][common.config["network"]][common.config["dex"]])