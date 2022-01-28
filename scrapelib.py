import pyperclip
from threading import Thread
from sniperlib import sniper
from time import sleep
from web3 import Web3
from common import log
class Scraper:

    def __init__(self) -> None:
        self.c = False
        Thread(target=self.clipboard).start()

    def toggle_C(self):
        self.c = not self.c
    
    def clipboard(self):
        previous = ""
        current = ""
        address = ""
        while True:
            if self.c:
                current = pyperclip.paste()
                if previous != current:
                    address = self.parse(current)
                    if address != None and address != "":
                        sniper.start(address)
                    previous = current
            sleep(0.01)

    def parse(self, string):
        string = str(string)
        main_message = string.split(' ')
        log.debug("Start parsing")
        for i in range(len(main_message)):
            log.debug(f"Iterated {i+1}/{len(main_message)}")
            if '0x' in main_message[i]:
                log.debug("Detected possible ETH address")
                try:
                    index = main_message[i].find('0x')
                    bottom_off = main_message[i][index:]
                    cut_off = bottom_off[:42].lower()
                    if "/tx" in main_message[i]:
                        log.debug("Ignoring as this is a tx.")
                        continue
                    if "dxsale.app" in main_message[i]:
                        log.debug("Ignoring as this is a dxsale link.")
                        continue
                    if "pinksale.finance" in main_message[i]:
                        log.debug("Ignoring as this is a PS link")
                        continue
                    if "g" in cut_off or "h" in cut_off or "i" in cut_off or "j" in cut_off or "k" in cut_off or "l" in cut_off or "m" in cut_off or "n" in cut_off or "o" in cut_off or "p" in cut_off or "q" in cut_off or "r" in cut_off or "s" in cut_off or "t" in cut_off or "u" in cut_off or "v" in cut_off or "w" in cut_off or "y" in cut_off or "z" in cut_off or "," in cut_off or "&" in cut_off:
                        log.debug("Ignoring as illegal chars were found.")
                        continue
                    if "add=" in main_message[i]:
                        log.debug("Ignoring as this is a dxsale link.")
                        continue
#                    if "dexscreener.com" in main_message[i]:
#                        log.debug("This is a Dexscreener link, attempting to parse address from LP")
#                        return Web3.toChecksumAddress(self.get_token_from_LP(Web3.toChecksumAddress(cut_off)))
                    if Web3.toChecksumAddress(cut_off) == "0x000000000000000000000000000000000000dEaD":
                        log.debug("Ignoring as this is the dead address.")
                        continue
                except ValueError:
                    log.debug("Invalid ETH-type address")
                    continue
                return Web3.toChecksumAddress(cut_off)

scraper = Scraper()
