from modules.apis.dnsbl import API
from modules.utils import pprint, colored
import argparse, sys


__doc__ = "Identifies spammers and the spambots they use to scrape addresses from your website."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("dnsbl", description=__doc__)
    parser.add_argument("host", type=str, help="Target hostname or ip address.")
    parser.add_argument("-k", "--api-key", type=str, help="Your HTTP:Bl Access Key.")
    args = parser.parse_args(args)
    
    try:
        dnsbl = API(args.api_key)
        info = dnsbl.query(args.host)
        if info["message"]:
            raise Exception(info["message"])
        print(colored("[i] DNSbl query results:"))
        pprint(info, 1, lambda x: x, "green", True)
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored(f"[!] Keyboard Interrupted!", "red"))

if __name__ == "__main__":
    parse_args()
