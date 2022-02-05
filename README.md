# same-old-boring-crypto-sniper

The title is enough of an explanation for what it is, I won't delve deeper in that.

## Disclaimer
It is your responsibility and choice that you're using this. You may lose money due to just crypto being crypto, or unexpected bugs. I won't be responsible in that case-nobody is forcing you to use this.  

## How do you run it?
There are a few steps to the setup.  
**This was only tested on Windows-unexpected issues can pop up with other OSes. Beware.**  
**Make sure you have Python 3.8 or greater installed!**
1. Install the necessary libraries(all are on pip): web3, pyperclip, webbrowser, flask.
2. Open `config.json` and input your
    * address
    * private key
    * optionally telegram API details(If you won't use Telegram, leave the API ID at 0.)
3. If you will use Telegram, follow these steps on your first time using the bot:
    1. run `python main.py --mode telegram` after entering your API details on `config.json`
    2. enter your phone number, code that Telegram sent you, and 2FA password if applicable.
    3. After getting the `Successfully logged in as <you>` message on the terminal, close the window.
4. Run `python main.py`, **without arguments**.
5. To configure your settings(amount, gas, network and dex), go to the Settings tab in the browser tab that opens.
---
**NOTE**

There are more settings than was said here-they are just not in the UI yet. To modify them, you can edit the JSON file manually.

---

## Which networks/chains are supported?
```
Network -> DEx
ropsten: uniswap
bsc_mainnet: pancakeswap_v2, biswap
ftm_mainnet: spiritswap, spookyswap
avax_mainnet: traderjoe, pangolin
cronos_mainnet: crodex, photonswap, cronical, cronoswap
moonbeam_mainnet: solarflare, dustydunes, padswap, stellaswap
```

## Is there a cost to it?
It's "free" to use, except that you have a 1% fee taken at every transaction.

## I have an idea/issue to report!
Open an issue in this repository. Issues are welcome if you put effort to it.

## License?
GPLv3.
