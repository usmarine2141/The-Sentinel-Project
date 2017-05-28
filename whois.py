from argparse import ArgumentParser
from modules.utils import colored
import socket, sys, re


__doc__ = "Executes whois queries against whois servers (obviously)."

def whois(server, port, query):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.send(f"{query}\r\n".encode())
    
    data = chunk = sock.recv(0xFFF)
    while chunk:
        chunk = sock.recv(0xFFF)
        data += chunk
    return data.decode("ascii", errors="replace")

def parse_args(args: list = sys.argv[1:]):
    parser = ArgumentParser("whois", description=__doc__, epilog="Tip: Query \"?\" to get a help message sent directly from the whois server ...")
    parser.add_argument("query", type=str, help="Query to be sent to the whois server.")
    parser.add_argument("-s", "--server", default="whois.iana.org", type=str, help="Server which to send the query (defaults to 'whois.iana.org').")
    parser.add_argument("-p", "--port", default=43, type=int, help="Port of the server which to send the query (defaults to 43).")
    args = parser.parse_args(args)
    
    try:
        answer = whois(args.server, args.port, args.query)
        server = re.search("whois\: (.*)", answer)
        if server:
            answer = whois(server.groups()[0].strip(), 43, args.query)
        for line in answer.split("\n"):
            print(colored(line, dark=line.startswith("%")))
    except Exception as e:
        print(colored(f"[!] Failed to execute whois query against \"{args.server}\" through port \"{args.port}\":", "red"))
        print(colored(" -  " + str(e), "red", True))

if __name__ == "__main__":
    parse_args()
