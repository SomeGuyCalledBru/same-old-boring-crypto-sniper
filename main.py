import http_api
import sys
try:
    if sys.argv[1] != '1':
        is_reset = "dont_start"
    else:
        is_reset = True
except IndexError:
    is_reset = False
if __name__ == "__main__":
    if is_reset != "dont_start":
        http_api.init(is_reset=is_reset)
    else:
        http_api.log.setLevel(50)
