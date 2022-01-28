import logging
import json
import colorama; colorama.init()
# Thank you SA ❤️
class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s[%(asctime)s]  %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d|%H:%M:%S")
        return formatter.format(record)
with open("config.json", "r") as f:
    config = json.load(f)

def generate_kwargs(**kwargs):
    return f'   {"".join([f"{i}={kwargs[i]}" for i in kwargs])}'
log = logging.getLogger('my_module_name')
log.setLevel(config["logSeverity"])
ch = logging.StreamHandler()
ch.setLevel(config["logSeverity"])
ch.setFormatter(CustomFormatter())
log.addHandler(ch)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)
