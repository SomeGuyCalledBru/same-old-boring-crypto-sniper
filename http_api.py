from audioop import mul
import logging


try:
    import os, sys
    from threading import Thread
    from flask import Flask, request, Response, send_from_directory
    from web3 import Web3
    import json
    import webbrowser
    from time import time, sleep
    import common
    import sniperlib
    import subprocess
    import scrapelib
except Exception as e:
    print(f"CRITICAL: An error occurred during start-up. Message: {e}\n Make sure that your configuration is correct and you have necessary libraries installed.\nIf you're sure everything is right, open an issue over at GitHub")
DECIMALS_CACHE = {}
PARAMS_CONVERTED = False
PORT = 9545
PRIVATE_INFORMATION = ["privateKey", "telegramApi"]
log = common.log
app = Flask(__name__)
sniper = sniperlib.sniper
scraper = scrapelib.scraper
@app.route("/")
def index():
    return send_from_directory('public', 'index.html')

@app.route("/<path:path>")
def main(path):
    return send_from_directory("public", path)

@app.route("/allNetworks")
def networks():
    return json.dumps(common.network_presets)

@app.route("/network")
def network():
    result = common.config["network"]
    return json.dumps(result)

@app.route("/dex")
def dex():
    result = common.config["dex"]
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
    return json.dumps(common.config)

@app.route("/isCoreConfigured")
def is_configured_core():
    return json.dumps(bool(common.config["address"]) and bool(common.config["privateKey"]))

@app.route("/isTGConfigured")
def is_tg_configured():
    log.debug(f'{bool(common.config["telegramApi"][0]) and bool(common.config["telegramApi"][1])}')
    return 'true' if bool(common.config["telegramApi"][0]) and bool(common.config["telegramApi"][1]) else 'false'

@app.route("/isDeployed")
def is_deployed():
    return json.dumps(common.main_contract != "0x0000000000000000000000000000000000000000")

@app.route("/simulate/<address>")
def simulate(address):
    return json.dumps(sniper.simulate(address, sniper.AMOUNT_TO_USE))

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
    return json.dumps({'simulations': sniper.simulations, 'trades': sniper.trades})

@app.route("/getBalance/<address>")
def get_balance(address):
    return json.dumps(sniper.get_token_balance(address))

@app.route("/getScrapeState/<_scraper>")
def get_scrape_state(_scraper):
    if _scraper == "c":
        return json.dumps(scraper.c)
    elif _scraper == "t":
        return json.dumps(scraper.t)

@app.route("/baseGas")
def base_gas():
    return json.dumps(sniper.base_gas_price)

@app.route("/getParams")
def get_params():
    return json.dumps({
        "amountUsed": sniper.AMOUNT_TO_USE,
        "gasParams": sniper.GAS_PARAMS
    })

@app.route("/setParams", methods=["POST"])
def set_params():
    AMOUNT_TO_USE = int(round(float(request.args.get('amount_used'))))
    GAS_PARAMS = json.loads(request.args.get('gas_params'))
    GAS_PARAMS[0] = int(round(float(GAS_PARAMS[0])))
    if None in GAS_PARAMS or AMOUNT_TO_USE == None:
        return Response('"Fields cannot be empty"', status=400)
    if GAS_PARAMS[1] < 50000:
        return Response('"Gas limit cannot be below 50K"', status=400)
    if GAS_PARAMS[0] < sniper.base_gas_price and not GAS_PARAMS[2]:
        return Response('"Gas price cannot be below base without adaptive gas enabled"', status=400)
    if AMOUNT_TO_USE == 0:
        return Response('"Amount cannot be zero"', status=400)
    sniper.set_params(AMOUNT_TO_USE, GAS_PARAMS)
    return '""'


@app.route("/deploy", methods=["POST"])
def deploy():
    return json.dumps(sniper.deploy())

@app.route("/deleteTrade/<side>/<index>", methods=["POST"])
def delete_trade(side, index):
    del sniper.trades[side][int(index)]
    sniper.set_trades()
    return '""'

@app.route("/restoreBuy/<address>", methods=["POST"])
def restore_buy(address):
    address = Web3.toChecksumAddress(address.replace(' ', ''))
    tx = request.args.get('tx').replace(' ', '')
    for i in sniper.trades["buy"]:
        log.debug(f"{i['tx']}, {tx}")
        if i["tx"] == tx and tx.startswith('0x'):
            return Response('"Tx already exists"', status=400)
    sniper.restore_buy(address, tx)
    return '""'

@app.route("/startSimulating/<address>", methods=["POST"])
def start_simulating(address):
    sniper.start(address, "manual input")
    return Response('""', status=202)

@app.route("/stopSimulating/<address>", methods=["POST"])
def stop_simulating(address):
    sniper.stop(address)
    return Response('""', status=200)

@app.route("/toggleScrape/<_scraper>", methods=["POST"])
def toggle_scrape(_scraper):
    if _scraper == "c":
        scraper.toggle_C()
    elif _scraper == "t":
        scraper.toggle_T()
    return '""'

@app.route("/buy", methods=["POST"])
def buy():
    """
    Buys token with provided parameters.
    Parameters:
    address[REQUIRED]: Address for token. 
    """
    if not request.args.get("address"):
        return '"Invalid request: required params missing"'
    return json.dumps(str(sniper.swap(Web3.toChecksumAddress(request.args.get("address").replace(" ", "")), "buy", Web3.toWei(sniper.AMOUNT_TO_USE, 'ether'), sniper.GAS_PARAMS, initiator="manual buy")))

@app.route("/sell", methods=["POST"])
def sell():
    """
    Sells token with provided parameters.
    address[REQUIRED]: Address for token. 
    amount_in[Optional]: Amount to sell. Everything is sold if unspecified.
    """
    if not request.args.get("address"):
        return '"Invalid request: required params missing"'
    return json.dumps(str(sniper.swap(Web3.toChecksumAddress(request.args.get("address").replace(" ", "")), "sell", request.args.get("amount_in", type=float), sniper.GAS_PARAMS, initiator="manual sell")))

@app.route("/pnl", methods=["GET"])
def pnl():
    return json.dumps(sniper.pnl(request.args.get("address"), request.args.get('in', type=int), request.args.get('out', type=int)))

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
    subprocess.Popen(["python", "main.py", "1"], close_fds=True)
    return Response('""', status=202)

@app.route("/set_ND", methods=["POST"])
def set_network_and_dex():
    if not network_dex_pair_valid(request.args.get("network"), request.args.get("dex")):
        return Response('"Invalid network-dex pair"', status=400)
    common.config["network"] = request.args.get("network")
    common.config["dex"] = request.args.get("dex")
    common.set_config()
    return '""'

@app.errorhandler(404)
def pnf(error):
    return f'Literally nothing to see here!', 404

@app.errorhandler(500)
def ise(error):
    return Response(f'"Whoops, you got us bad. Something must not have happened but it happened anyway. Error: {error}"', status=500)

def _kill():
    sleep(0.1)
    log.debug("Rekting")
    os._exit(1)

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
    app.run(host="127.0.0.1", port=PORT)
