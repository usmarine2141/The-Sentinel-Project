import urllib.parse, requests, argparse, sys
from modules.utils import colored, pprint
from modules.heartbleed import Heartbleed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


__doc__ = "Web Server Fingerprinting Tool."

checks = {"Cloudflare": lambda resp: resp.headers.get("Server") == "cloudflare-nginx" or
                                     "CF-RAY" in resp.headers or
                                     "__cfduid" in resp.cookies,
          "WebKnight": lambda resp: "webknight/" in resp.headers.get("Server", "").lower() or
                                     resp.status_code == 999,
          "Airlock": lambda resp: "AL_LB" in resp.cookies or
                                  "AL_SESS" in resp.cookies,
          "Barracuda": lambda resp: "barra_counter_session" in resp.cookies,
          "Denyall": lambda resp: "sessioncookie" in resp.cookies,
          "F5 Traffic Shield": lambda resp: resp.headers.get("Server") == "F5-TrafficShield" or
                                            "ASINFO" in resp.cookies,
          "Teros / Citrix Application Firewall Enterprise": lambda resp: "st8id" in resp.cookies or
                                                                         "st8_wat" in resp.cookies or
                                                                         "st8_wlf" in resp.cookies,
          "BinarySec": lambda resp: "binarysec/" in resp.headers.get("Server", "").lower() or
                                     "x-binarysec-via" in resp.headers or
                                     "x-binarysec-nocache" in resp.headers,
          "Profense": lambda resp: resp.headers.get("Server") == "Profense" or
                                   "PLBSID" in resp.cookies,
          "Citrix Netscaler": lambda resp: "ns_af" in resp.cookies or
                                           "citrix_ns_id" in resp.cookies or
                                           any([cookie.name.startswith("NSC_") for cookie in resp.cookies]),
          "dotDefender": lambda resp: str(resp.headers.get("X-dotdefender-denied")) == "1",
          "IBM DataPower": lambda resp: "x-backside-transport" in resp.headers,
          "Incapsula WAF": lambda resp: any([cookie.name.startswith("incap_ses") or cookie.name.startswith("visid_incap") for cookie in resp.cookies]),
          "USP Secure Entry Server": lambda resp: resp.headers.get("Server") == "Secure Entry Server",
          "Cisco ACE XML Gateway": lambda resp: resp.headers.get("Server") == "ACE XML Gateway",
          "ModSecurity": lambda resp: "mod_security/" in resp.headers.get("Server", "").lower() or
                                       resp.headers.get("Server") == "NOYB",
          "F5 BigIP": lambda resp: "x-cnection" in resp.headers or
                                   resp.headers.get("Server") == "BigIP" or
                                   "BIGipServer" in resp.cookies,
          }

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("wserfpt", description=__doc__)
    parser.add_argument("url", type=str, help="Target URL.")
    args = parser.parse_args(args)
    
    session = requests.Session()
    try:
        head = session.head(args.url, verify=True)
    except requests.exceptions.SSLError as e:
        print(colored(f"[{type(e).__name__}] {str(e)[0].upper() + str(e)[1:]}", "yellow"))
        head = session.head(args.url, verify=False)
        print("")
    
    try:
        if Heartbleed(args.url).vulnerable:
            print(colored(f"[!] Target is affected by the Heartbleed Bug!", "red"))
            print("")
    except:
        pass
    
    print(colored(f"[i] HEAD Response Info.:"))
    pprint({"Version": f"HTTP/{'{0[0]}.{0[0]}'.format(str(head.raw.version))}", "Status": f"{head.status_code} {head.reason}",
            "Closed": head.raw.closed, "Chunked": head.raw.chunked,
            "Readable": head.raw.readable(), "Seekable": head.raw.seekable(), "Writable": head.raw.writable(),
            "Apparent Encoding": head.apparent_encoding, "Encoding": head.encoding,
            "Is Redirect": head.is_redirect, "Is Permanent Redirect": head.is_permanent_redirect,
            "Enforce Content Length": head.raw.enforce_content_length,
            "Retries": head.raw.retries.total}, title=False)
    
    headers = dict(head.headers)
    for name in ["Set-Cookie", "Link"]:
        while name in headers:
            del headers[name]
    
    if head.links:
        print("")
        print(colored(f"[i] Server Links: ({len(head.links)})"))
        pprint(head.links)
    
    if headers:
        print("")
        print(colored(f"[i] Server Headers: ({len(headers)})"))
        pprint(headers)
    
    if head.cookies:
        cookies = {}
        print("")
        print(colored(f"[i] Server Cookies: ({len(head.cookies)})"))
        for cookie in sorted(head.cookies, key=lambda x: x.name):
            name, value = cookie.name, cookie.value
            tags = tuple(sorted(set(["Secure" if cookie.secure else "Insecure"] + list(cookie._rest.keys()))))
            cookies[name] = {"tags": tags, "value": value}
            #print(colored(f" -  [{', '.join(tags)}] {name}: ") + colored(f"{value[:79] + '[...]' if len(value) > (79 - len(name)) else value}", dark=True))
        pprint(cookies)
    
    responses = []
    try:
        options = session.options(args.url).headers.get("Allow").split(",")
    except:
        options = []
        for method in ["GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]:
            try:
                resp = session.request(method, args.url)
                if resp.status_code != 405:
                    options.append(method)
                responses.append(resp)
            except:
                pass
    print(colored("\n[i] Supported request methods: ") + colored(f"{', '.join(sorted(options))}", dark=True))
    
    firewalls = []
    for resp in responses:
        for name, check in sorted(checks.items(), key=lambda x: x[0]):
            if name not in firewalls:
                detected = check(resp)
                if detected:
                    firewalls.append(name)
    if firewalls:
        print(colored(f"[i] Detected Web Application Firewall{'s' if len(firewalls) != 1 else ''}: {', '.join(firewalls)}"))
    
    resp_times = [resp.elapsed.total_seconds() for resp in responses]
    if resp_times:
        print("")
        print(colored("[i] Response Times Summary (in seconds):"))
        print(colored(f" -  Minimum: {min(resp_times):.02f}s   -   Average: {float(sum(resp_times)) / max(len(resp_times), 1):.02f}s   -   Maximum: {max(resp_times):.02f}s", dark=True))

if __name__ == "__main__":
    try:
        parse_args()
    except (Exception, KeyboardInterrupt) as e:
        print(colored(f"[!] {type(e).__name__}" + (":" if e else ""), "red"))
        if e:
            print(colored(f" -  {e}", "red", True))
