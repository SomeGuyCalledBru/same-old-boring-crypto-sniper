try:
    import os, sys
    from threading import Thread
    from flask import Flask, request, Response, send_from_directory
    from web3 import Web3
    from common import log, generate_kwargs
    import common
    import json
    from sniperlib import sniper
    import webbrowser
    from time import time, sleep
    from scrapelib import scraper
except Exception as e:
    print(f"CRITICAL: An error occurred during start-up. Message: {e}\n Make sure that your configuration is correct and you have necessary libraries installed.\nIf you're sure everything is right, open an issue over at GitHub")
DECIMALS_CACHE = {}
PORT = 9545
PRIVATE_INFORMATION = ["privateKey", "telegramApi"]
app = Flask(__name__)

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
    return json.dumps(bool(common.config["telegramApi"][0]) and bool(common.config["telegramApi"][1]))

@app.route("/isDeployed")
def is_deployed():
    return json.dumps(common.main_contract != "0x0000000000000000000000000000000000000000")

@app.route("/simulate/<address>")
def simulate(address):
    return json.dumps(sniper.simulate(address))

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
    log.debug("getSimulationsAndTrades")
    return json.dumps({'simulations': sniper.simulations, 'trades': sniper.trades})

@app.route("/getBalance/<address>")
def get_balance(address):
    return json.dumps(sniper.get_token_balance(address))

@app.route("/getScrapeState/<_scraper>")
def get_scrape_state(_scraper):
    if _scraper == "c":
        return json.dumps(scraper.c)

@app.route("/setConfig", methods=["POST"])
def set_config():
    with open("config.json", "w") as f:
        json.dump(request.args.to_dict(), f, indent=4)
    return json.dumps('""')

@app.route("/deploy", methods=["POST"])
def deploy():
    return json.dumps(sniper.deploy())

@app.route("/deleteTrade/<side>/<index>", methods=["POST"])
def delete_trade(side, index):
    del sniper.trades[side][int(index)]
    sniper.set_trades()
    return '""'

@app.route("/startSimulating/<address>", methods=["POST"])
def start_simulating(address):
    sniper.start(address)
    return Response('""', status=202)

@app.route("/stopSimulating/<address>", methods=["POST"])
def stop_simulating(address):
    sniper.stop(address)
    return Response('""', status=200)

@app.route("/toggleScrape/<_scraper>", methods=["POST"])
def toggle_scrape(_scraper):
    if _scraper == "c":
        scraper.toggle_C()
    return '""'

@app.route("/buy", methods=["POST"])
def buy():
    """
    Buys token with provided parameters.
    Parameters:
    address[REQUIRED]: Address for token. 
    amount_in[Optional]: If specified, overrides spec in configuration.
    """
    if not request.args.get("address"):
        return '"Invalid request: required params missing"'
    return json.dumps(str(sniper.swap(Web3.toChecksumAddress(request.args.get("address").replace(" ", "")), "buy", amount_in=Web3.toWei(request.args.get("amount_in", type=float), 'ether') if request.args.get("amount_in", type=float) != None else None)))

@app.route("/sell", methods=["POST"])
def sell():
    """
    Sells token with provided parameters.
    address[REQUIRED]: Address for token. 
    amount_in[Optional]: Amount to sell. Everything is sold if unspecified.
    """
    if not request.args.get("address"):
        return '"Invalid request: required params missing"'
    return json.dumps(str(sniper.swap(Web3.toChecksumAddress(request.args.get("address").replace(" ", "")),  side="sell", amount_in=request.args.get("amount_in", type=float))))

@app.route("/pnl", methods=["GET"])
def pnl():
    return json.dumps(sniper.pnl(request.args.get("address"), request.args.get('in', type=int), request.args.get('out', type=int)))

@app.route("/ping", methods=["GET"])
def ping():
    """
    Does nothing but serve as a ping endpoint.
    """
    if not common.w3.isConnected():
        return Response('""', status=418)
    return Response('""', status=200)

@app.route("/kill", methods=["POST"])
def kill():
    Thread(target=_kill).start()

def _kill():
    sleep(0.5)
    os._exit(1)

def init():
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT)
