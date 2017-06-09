from modules.session import Session
from modules.utils import colored, pprint
import urllib.parse, argparse, sys, os


__doc__ = "Traces the route that HTTP requests goes through on a specific server ..."
term_size = os.get_terminal_size().columns

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("http-tracert", description=__doc__)
    parser.add_argument("url", type=str, help="The URL to send requests to.")
    parser.add_argument("-m", "--method", type=str, default="GET", help="HTTP request method to use. Defaults to GET. Among other values, TRACE is probably the most interesting.")
    parser.add_argument("-x", "--max-forwards", type=int, default=3, help="Maximum number of forwards to follow ...")
    args = parser.parse_args(args)
    
    try:
        last_response = None
        checked = {}
        session = Session(args.url)
        print(colored(f"[i] Tracing {args.max_forwards} HTTP requests to {repr(session.base_url.netloc)}:"))
        for hop in range(args.max_forwards + 1):
            response = session.request(args.method, "", headers={"Max-Forwards": str(hop), "No-Cache": "true"})
            headers = dict(response.headers)
            title = session.parse_html(response.content).title
            print(colored(f"[+] HOP #{hop:02}: {urllib.parse.urlparse(response.url).netloc} - {response.status_code} {response.reason}"))
            if last_response is not None and (True if (title and title.text == session.parse_html(last_response.content).title.text) else True) and (
                response.status_code == last_response.status_code and response.reason == last_response.reason and response.url == last_response.url and
                response.headers.get("Server") == last_response.headers.get("Server")):
                print(colored("    ..."))
            else:
                if title:
                    if last_response and title.text == session.parse_html(last_response.content).title.text:
                        pass
                    else:
                        print(colored(f" -  Page Title: ") + colored(title.text, dark=True))
                if checked:
                    print(colored("    ..."))
                for key, value in headers.items():
                    if key in checked and checked[key] == value:
                        continue
                    value = colored(value[:term_size - (len(key) + 12)], dark=True) + colored("[...]") if len(value) > term_size - (len(key) + 12) else colored(value, dark=True)
                    print(colored(f" -  {key.title()}: ") + value)
                checked.update(headers)
            last_response = response
            print("")
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))

if __name__ == "__main__":
    parse_args()
