
# same-old-boring-crypto-sniper
The title is enough of an explanation for what it is, I won't delve deeper in that.

## This project is going closed source on next release - reasons will be explained when the release actually happens.

## Disclaimer
It is your responsibility and choice that you're using this. You may lose money due to just crypto being crypto, or unexpected bugs. I won't be responsible in that case-nobody is forcing you to use this.  

## How do you run it?
There are a few steps to the setup.  
**This was only tested on Windows-unexpected issues can pop up with other OSes. Beware.**  
**Make sure you have Python 3.8 or greater installed!**
1. Install the necessary libraries(all are on pip): ```pip(3) install web3, pyperclip, webbrowser, flask, telethon```
2. Open `config.json` and input your
    * address
    * private key
    * optionally telegram API details(If you won't use Telegram, leave the API ID at 0.)
3. If you will use Telegram, follow these steps on your first time using the bot:
    1. run `python main.py telegram` after entering your API details on `config.json`
    2. enter your phone number, code that Telegram sent you, and 2FA password if applicable.
    3. After getting the `Successfully logged in as <you>` message on the terminal, close the window.
4. Run `python main.py`, **without arguments**.
5. To configure your settings(amount, gas, network and dex), go to the Settings tab in the browser tab that opens.
---
**NOTE**
* If you've known any programming language for more than a few seconds, 
you may have noticed that the section that is open-sourced is 
basically just a web server, thus you might
feel intrigued to open it up to the world to use this remotely.
**Don't!** Not only is it a security nightmare that gives people control over
your wallet, it's just not designed to run that way.

---

## Is there a cost to it?
You pay as you use with a 1% fee on every transaction you do.

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

## I have an idea/issue to report!
Open an issue in this repository. Issues are welcome if you put effort to it.

## License?
GPLv3.
