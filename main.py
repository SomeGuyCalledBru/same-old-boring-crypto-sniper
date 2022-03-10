import http_api, common
import sys
try:
    startup_mode = sys.argv[1] if sys.argv[1] in ["standard", "restart", "telegram"] else "standard"
except IndexError:
    startup_mode = "standard"
if __name__ == "__main__":
    if startup_mode == "standard":
        http_api.init(is_reset=False)
    elif startup_mode == "restart":
        http_api.init(is_reset=True)
    elif startup_mode == "telegram":
        # Don't start HTTP API&silence logs to let user enter info
        common.log.setLevel(50)