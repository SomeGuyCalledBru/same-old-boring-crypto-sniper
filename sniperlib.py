from time import time, sleep
from web3 import Web3
from common import log, w3, config, network_presets
import common
from threading import Thread
import json
NULL = "0x0000000000000000000000000000000000000000"
class Sniper:
    def __init__(self, config, network, dex):
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
        self.bootstrap_pending_trades() # The user can interrupt the bot while some transactions are pending. To not leave them hanging in later runs, this function's used.
        self.base_gas_price = 0
        Thread(target=self.fetch_base_gas_price, args=(5,)).start()

    def deploy(self):
        tx = self.factory.functions.deploy()
        data = self.construct_tx_dict(1000000, Web3.toWei(5, 'gwei'), 0, True)
        built_tx = tx.buildTransaction(data)
        signed_tx = w3.eth.account.sign_transaction(built_tx, self.config["privateKey"])
        return Web3.toHex(w3.eth.sendRawTransaction(signed_tx.rawTransaction))

    def pnl(self, address, amount_in, amount_out):
        result = self.router.functions.getAmountsOut(amount_out, self.construct_path(address, NULL, "sell")).call()[-1]
        mul = round(result/amount_in, 5)
        return {
            "multiplier": mul,
            "percentage_string": f"{round((mul-1)*100, 4)}%",
            "if_sold_now": int(mul*amount_in)
        }

    def start(self, address, amount_in=None):
        # amount_in is in wei
        Thread(target=self._start, args=(Web3.toChecksumAddress(address.replace(" ", "")), amount_in)).start()

    def stop(self, address):
        del self.simulations[address]

    def _start(self, address, amount_in=None):
        # meant to be called outside main thread.
        try:
            if amount_in == None: amount_in = self.config["amountUsed"]
            try:
                if self.simulations[address] == "Running": return
            except Exception:
                pass
            if len([i for i in self.simulations if i == "Running"]) >= 5:
                return
            self.simulations[address] = "Running"
            while True:
                result = self.simulate(address)
                if result or self.simulations[address] != "Running":
                    break
                sleep(self.config["intervalBetweenSimulationsMs"]/1000)
            if self.simulations[address] == "Running":
                self.swap(address, "buy", amount_in=amount_in)
                self.simulations[address] = "Succeeded!"
        except KeyError as e:
            if address in str(e):
                pass
            else:
                self.simulations[address] = "Errored"
                return
        except Exception:
            self.simulations[address] = "Errored"
            return

    def simulate(self, address):
        path = self.construct_path(address, NULL, "buy")
        log.debug([self.dex["router"], path, path[::-1], self.config["simulationTaxLimitPercent"]])
        calldata = self.simulator.encodeABI(fn_name='checkNow', args=[self.dex["router"], path, path[::-1], self.config["simulationTaxLimitPercent"]])
        try:
            w3.eth.call({"from": self.config["address"], "to": self.simulator.address, "data": calldata, "value": self.config["amountUsed"]})
            return True
        except Exception as e:
            log.warning(f"Exception in simulation, returning False: {e}")
            return False

    def swap(self, address, side, amount_in=None):
        """
        address: Token to buy.
        amount_in: Amount input in WEI form if a buy, or in PERCENTAGE if a sell.
        side: Buy or sell."""
        # Load the encoder specified, just in case the DEX isn't uni v2 compatible.
        encoder = common.encoders[self.dex["encoder"]] 
        if amount_in == None:
            amount_in = self.config["amountUsed"] if side == "buy" else self.get_token_balance(address)
        elif amount_in != None and side == "sell":
            perc = amount_in
            amount_in = int(self.get_token_balance(address)*perc/100)
        # No action is necessary if the amount is specified and it's a buy.
        path = self.construct_path(address, NULL, side)
        # Encode calldata with the encoder function, specified for that DEX.
        calldata = encoder(int(amount_in*99/100) if side == "buy" else amount_in, path, common.main_contract, self.dex["router"])
        # Standard transaction signing procedures
        tx_data = self.construct_tx_dict(self.config[f"gas@{side}"], self.config[f"gasPrice@{side}"], amount_in if side == "buy" else 0, self.config["adaptiveGasStrategy"])
        contract_transaction = self.contract.functions.swap(self.dex["router"], calldata, path[0], path[-1], side == "sell")
        built_transaction = contract_transaction.buildTransaction(tx_data)
        signed_transaction = w3.eth.account.sign_transaction(built_transaction, self.config["privateKey"])
        transaction_hash = Web3.toHex(w3.eth.sendRawTransaction(signed_transaction.rawTransaction))
        self.trades[side].insert(0, {
            "address": address,
            "status": "Pending",
            "tx": transaction_hash,
            "amount_in": amount_in,
            "amount_out": -1
        })
        self.set_trades()
        self.update_trade(transaction_hash, side)
        return transaction_hash

    def construct_tx_dict(self, gas_limit, gas_price, value, adaptive_gas): 
        """Returns a full transaction data dictionary from config and parameters."""
        result = {
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

    def fetch_base_gas_price(self): 
        while True:
            try:
                result = w3.eth.get_block('latest').baseFeePerGas if self.network["eip1559"] else w3.eth.gas_price
                self.base_gas_price = result
                log.info(f"Updated base gas, result: {result}")
            except Exception as e:
                log.warning(f"Failed to update base gas, error: {e}")
            sleep(5)

    def get_token_balance(self, address): """Returns the token balance in the contract."""; return w3.eth.contract(address=address, abi=common.erc_abi).functions.balanceOf(common.main_contract).call()
    def decs(self, address): """Returns the token decimals."""; return w3.eth.contract(address=address, abi=common.erc_abi).functions.decimals().call()
    def bootstrap_pending_trades(self):
        for i in self.trades["buy"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "buy")
        for i in self.trades["sell"]:
            if i["status"] == "Pending":
                self.update_trade(i["tx"], "sell")

    def update_trade(self, tx_hash, side): Thread(target=self._update_trade, args=(tx_hash, side)).start()
    def _update_trade(self, tx_hash, side):
        # TODO: add a trade tracker to restart checker on startup
        if side == "buy":
            for i in range(len(self.trades["buy"])):
                # Get the matching trade by iterating through it
                if self.trades["buy"][i]["tx"] == tx_hash:
                    address = self.trades["buy"][i]["address"]
                    token_contract = w3.eth.contract(address=address, abi=common.erc_abi)
                    # Wait for the transaction receipt. We're interested in the status and the logs.
                    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                    # Report a failed transaction.
                    if not tx_receipt.status:
                        self.trades["buy"][i]["status"] = "Failed"
                        self.set_trades()
                        return
                    # If we succeeded, we can move on.
                    logs = token_contract.events.Transfer().processReceipt(tx_receipt)
                    totalOutput = 0
                    for log in logs:
                        # If a log:
                        # - is emitted from the target token
                        # - is a transfer with the destination as the contract wallet
                        # then we can say it's a valid output.
                        if Web3.toChecksumAddress(log.args.to) == self.contract.address and Web3.toChecksumAddress(address) == log.address:
                            totalOutput += log.args.value
                    # Update the necessary values and return
                    self.trades["buy"][i]["status"] = "Successful"
                    self.trades["buy"][i]["amount_out"] = totalOutput
                    self.set_trades()
                    return 
        elif side == "sell":
            for i in range(len(self.trades["sell"])):
                # Get the matching trade by iterating through it
                if self.trades["sell"][i]["tx"] == tx_hash:
                    WETH_contract = w3.eth.contract(address=self.WETH, abi=common.erc_abi)
                    # Wait for the transaction receipt. We're interested in the status and the logs.
                    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=86400, poll_latency=1)
                    # Report a failed transaction.
                    if not tx_receipt.status:
                        self.trades["sell"][i]["status"] = "Failed"
                        self.set_trades()
                        return
                    # If we succeeded, we can move on.
                    logs = WETH_contract.events.Transfer().processReceipt(tx_receipt)
                    totalOutput = 0
                    for log in logs:
                        # If a log:
                        # - is emitted from the target token
                        # - is a transfer with the destination as the contract wallet
                        # then we can say it's a valid output.
                        if Web3.toChecksumAddress(log.args.to) == self.contract.address and self.WETH == log.address:
                            totalOutput += log.args.value
                    # Update the necessary values and return
                    self.trades["sell"][i]["status"] = "Successful"
                    self.trades["sell"][i]["amount_out"] = totalOutput
                    self.set_trades()
                    return 
    def set_trades(self): 
        with open(f"trades-{config['network']}-{config['dex']}.json", "w") as f: 
            json.dump(self.trades, f, indent=4)
# Had to move out due to circular imports
sniper = Sniper(config=config, network=network_presets["networks"][config["network"]], dex=network_presets["dexes"][config["network"]][config["dex"]])
