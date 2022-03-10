try:
    from traceback import format_exc
    import os, shutil, signal, subprocess, webbrowser
    from threading import Thread
    from flask import Flask, request, Response, send_from_directory
    from web3 import Web3
    import json
    from time import sleep
    import common
    import sniperlib
    import scrapelib
    import re
except Exception as e:
    print(f"CRITICAL: An error occurred during start-up. Message: \n{format_exc()}\n Make sure that your configuration is correct and you have necessary libraries installed.\nIf you're sure everything is right, open an issue over at GitHub")
DECIMALS_CACHE = {}
VALIDATION_CACHE = {}
PARAMS_CONVERTED = False
PORT = 9545
PRIVATE_INFORMATION = ["privateKey", "telegramApi"]
app = Flask(__name__)
sniper = sniperlib.sniper
scraper = scrapelib.scraper
@app.route("/")
def index():
    return send_from_directory('public', 'index.html')

@app.route("/<path:path>")
def main(path):
    return send_from_directory("public", path)

@app.route("/pingRpc")
def ping_rpc():
    try:
        if request.args.get("rpcUrl"):
            web3 = Web3(Web3.HTTPProvider(request.args.get("rpcUrl")))
            cid = web3.eth.chain_id
            common.log.info(f"Chain ID: {cid}")
            if cid != sniper.chain_id:
                raise Exception(f"This RPC isn't for this network. (CID: Expected {sniper.chain_id}, got {cid})")
        return '"OK"'
    except Exception as e:
        return f'"{e}"', 400
        
@app.route("/allNetworks")
def networks():
    return json.dumps(common.network_presets)

@app.route("/network")
def network():
    result = sniper.config["network"]
    return json.dumps(result)

@app.route("/dex")
def dex():
    result = sniper.config["dex"]
    return json.dumps(result)

@app.route("/txReceipt/<hash>")
def tx_receipt(hash):
    try:
        result = common.w3.eth.get_transaction_receipt(hash)
        return json.dumps((True, result.status))
    except Exception as e:
        return json.dumps((False, 0))

@app.route("/getConfig")
def get_config():
    return json.dumps(sniper.config)

@app.route("/isCoreConfigured")
def is_configured_core():
    return json.dumps(bool(int(sniper.config["address"], 16)) and bool(int(sniper.config["privateKey"], 16)))

@app.route("/isTGConfigured")
def is_tg_configured():
    return 'true' if bool(sniper.config["telegramApi"]["API_ID"]) and bool(sniper.config["telegramApi"]["API_HASH"]) else 'false'

@app.route("/isDeployed")
def is_deployed():
    return json.dumps(common.main_contract != "0x0000000000000000000000000000000000000000")

@app.route("/decs/<address>")
def decimals(address):
    global DECIMALS_CACHE
    try:
        return json.dumps(DECIMALS_CACHE[address])
    except KeyError:
        decs = sniper.decs(address)
        DECIMALS_CACHE[address] = decs
        return json.dumps(decs)

@app.route("/getSimulationsAndTrades")  
def get_simulations():
    return json.dumps({'simulations': sniper.simulations, 'trades': sniper.trades, 'price': sniper.ticker_price})

@app.route("/getBalance/<address>")
def get_balance(address):
    return json.dumps(sniper.get_token_balance(address))
    
@app.route("/getScrapeState/<_scraper>")
def get_scrape_state(_scraper):
    return json.dumps(scraper.toggles[_scraper])

@app.route("/baseGas")
def base_gas():
    return json.dumps(sniper.base_gas_price)

@app.route("/getParams")
def get_params():
    return json.dumps({
        "amountUsed": sniper.config["AMOUNT_TO_USE_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][sniper.config["network"]],
        "gasParams": sniper.config["GAS_PARAMETERS_DO_NOT_MODIFY_IT_HERE_OR_YOU_WILL_GET_REKT"][sniper.config["network"]],
        "amountUnit": sniper.config["amountUnit"][sniper.config["network"]]
    })

@app.route("/mempoolCompatible")
def mempool_compatible():
    return json.dumps(sniper.txpool_support)

@app.route("/getOutput")
def get_output():
    return json.dumps(sniper.get_output(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), request.args.get("side"), request.args.get("amount", type=int)))

@app.route("/getPrice")
def get_price():
    return json.dumps(sniper.get_price(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), request.args.get("is_usd") == "true", request.args.get("decimals", type=int)))

@app.route("/createOrder", methods=["POST"])
def create_order():
    if request.args.get("orderType") == "limit":
        sniper.set_limit(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), request.args.get("side"), request.args.get("type"), request.args.get("amount", type=float), request.args.get("amount_unit"), request.args.get("price", type=float), request.args.get("price_unit"))
    elif request.args.get("orderType") == "market":
        sniper.set_market(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), request.args.get("side"), request.args.get("amount", type=float), request.args.get("amount_unit"))
    elif request.args.get("orderType") == "stdSnipe":
        sniper.start_snipe(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), "stdSnipe", request.args.get("amount", type=float), request.args.get("amount_unit"), initiator="standard snipe")
    elif request.args.get("orderType") == "memSnipe":
        if sniper.txpool_support:
            sniper.start_snipe(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')), "memSnipe", request.args.get("amount", type=float), request.args.get("amount_unit"), initiator="mempool snipe", rules=json.loads(request.args.get("rules")))    
        else:
            return '"Mempool not supported"', 400
    return '""'

@app.route("/deleteLimitOrder", methods=["POST"])
def delete_limit_order():
    sniper.delete_limit(int(request.args.get("index")))

@app.route("/validateContractAddress")
def validate_contract_address():
    global VALIDATION_CACHE
    try:
        return VALIDATION_CACHE[Web3.toChecksumAddress(request.args.get("address").replace(' ', ''))]
    except KeyError:
        common.log.info(f"Cache for {Web3.toChecksumAddress(request.args.get('address').replace(' ', ''))} not found. Validating...")
        try: 
            sniper.get_token_balance(Web3.toChecksumAddress(request.args.get("address").replace(' ', '')))
            VALIDATION_CACHE[Web3.toChecksumAddress(request.args.get("address").replace(' ', ''))] = 'true'
            common.log.info(f"{Web3.toChecksumAddress(request.args.get('address').replace(' ', ''))} is a valid token address.")
            return 'true'
        except Exception as e:
            VALIDATION_CACHE[Web3.toChecksumAddress(request.args.get("address").replace(' ', ''))] = 'false'
            common.log.info(f"{Web3.toChecksumAddress(request.args.get('address').replace(' ', ''))} is not a valid token address.")
            return 'false'
    except ValueError:
        # This means the address is invalid, don't cache anything and return false
        return 'false'
@app.route("/setParams", methods=["POST"])
def set_params():
    AMOUNT_TO_USE = float(request.args.get("amount_used"))
    AMOUNT_UNIT = request.args.get("amount_unit")
    GAS_PARAMS = json.loads(request.args.get('gas_params'))
    GAS_PARAMS[0] = int(round(float(GAS_PARAMS[0])))
    if None in GAS_PARAMS:
        return Response('"Fields cannot be empty"', status=400)
    if GAS_PARAMS[1] < 50000:
        return Response('"Gas limit cannot be below 50K"', status=400)
    if GAS_PARAMS[0] < sniper.base_gas_price and not GAS_PARAMS[2]:
        return Response('"Gas price cannot be below base without adaptive gas enabled"', status=400)
    sniper.set_params(AMOUNT_TO_USE, GAS_PARAMS, AMOUNT_UNIT)
    return '""'

@app.route("/setMisc", methods=["POST"])
def set_misc():
    # PARAMS:
    # method: The method to use. Can be "set", "append", "index" or "remove"(defaults to "set") 
    # key: The key to modify
    # value: The value to set(required if method is "set" or "append")
    # index: The index to modify(required if method is "index")
    # instant_apply: Whether to apply the change immediately(defaults to false)

    if request.args.get("method") in [None, "set"]:
        value_type = str if not is_number(request.args.get("value")) else int if float(request.args.get("value")) % 1 == 0 else float 
        sniper.config[request.args.get("key")] = request.args.get('value', type=value_type)
        sniper.set_config()
        return '""'
    elif request.args.get("method") == "append":
        sniper.config[request.args.get("key")].append("")
        sniper.set_config()
        return '""'
    elif request.args.get("method") == "index":
        value_type = str if not is_number(request.args.get("value")) else int if float(request.args.get("value")) % 1 == 0 else float 
        index_type = str if not is_number(request.args.get("index")) else int if float(request.args.get("index")) % 1 == 0 else float 
        sniper.config[request.args.get("key")][request.args.get("index", type=index_type)] = request.args.get("value", type=value_type)
        sniper.set_config()
        return '""'
    elif request.args.get("method") == "remove":
        if request.args.get("index") != None:
            index_type = str if not is_number(request.args.get("index")) else int if float(request.args.get("index")) % 1 == 0 else float 
            del sniper.config[request.args.get("key")][request.args.get("index", type=index_type)]
        else:
            del sniper.config[request.args.get("key")]
        sniper.set_config()
        return '""'
    else:
        return Response('"Invalid instruction"', status=400)
    

@app.route("/deploy", methods=["POST"])
def deploy():
    return json.dumps(sniper.deploy())

@app.route("/deleteTrade/<side>/<index>", methods=["POST"])
def delete_trade(side, index):
    sniper.delete_trade(side, int(index))
    return '""'

@app.route("/validateMethodID")
def validate_method_id():
    if re.match(r"0x[0-9a-fA-F]{8}", request.args.get("method_id")):
        return "true"
    else:
        return "false"

@app.route("/restoreTrade/<address>", methods=["POST"])
def restore_trade(address):
    address = Web3.toChecksumAddress(address.replace(' ', ''))
    sniper.restore_trade(address)
    return '""'

@app.route("/stopSimulating/<ident>", methods=["POST"])
def stop_simulating(ident):
    sniper.stop_standard_snipe(ident)
    return Response('""', status=200)

@app.route("/toggleScrape/<_scraper>", methods=["POST"])
def toggle_scrape(_scraper):
    scraper.toggle(_scraper)
    return '""'
    
@app.route("/pnl", methods=["GET"])
def pnl():
    result = sniper.address_only_pnl(Web3.toChecksumAddress(request.args.get("address").replace(" ", "")))
    if result == None:
        return "false", 400
    return json.dumps(result)

@app.route("/ping", methods=["GET"])
def ping():
    """
    Does nothing but serve as a ping endpoint.
    """
    if not common.w3.isConnected():
        return Response('""', status=503)
    return Response('""', status=200)

@app.route("/kill", methods=["POST"])
def kill():
    Thread(target=_kill).start()
    subprocess.Popen([f"python{'' if shutil.which('python') != None else '3'}", "main.py", "restart"], close_fds=True)
    return Response('""', status=202)

@app.route("/set_ND", methods=["POST"])
def set_network_and_dex():
    global VALIDATION_CACHE, DECIMALS_CACHE
    if not network_dex_pair_valid(request.args.get("network"), request.args.get("dex")):
        return Response('"Invalid network-dex pair"', status=400)
    sniper.reinit(request.args.get("network"), request.args.get("dex"))
    # Clear cache to avoid conflicts
    VALIDATION_CACHE = {}
    DECIMALS_CACHE = {}
    return '""'

@app.errorhandler(404)
def pnf(error):
    return f'Literally nothing to see here!', 404

@app.errorhandler(429)
def too_many_requests(error):
    return Response('"Too many requests"', status=429)

@app.errorhandler(500)
def internal_server_error(error):
    return Response(f'"Internal server error: {error}"', status=500)

# Check if is number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def _kill():
    sleep(0.1)
    common.log.debug("Rekting")
    os.kill(os.getpid(), signal.SIGINT)

def network_dex_pair_valid(network, dex):
    try:
        common.network_presets["dexes"][network][dex]["name"]
        return True
    except Exception:
        return False

def init(is_reset):
    # Let port free on restart
    if is_reset:
        sleep(1)
    else:
        webbrowser.open("http://127.0.0.1:9545")
    try:
        app.run(host="127.0.0.1", port=PORT)
    except KeyboardInterrupt:
        common.log.info("Got interrupt, cleaning up")
        sniper.set_trades()
        common.log.info("Bye!")
