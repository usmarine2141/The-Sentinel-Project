import argparse, sys
from modules import pyping


debug = False
__doc__ = """A pure python ping implementation using raw sockets.

Note that ICMP messages can only be send from processes running as root
(in Windows, you must run this script as 'Administrator').
"""

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("ping", description=__doc__)
    parser.add_argument("host", type=str, help="Target hostname or ip address.")
    parser.add_argument("-t", "--timeout", type=int, default=1000, help="Timeout in ms to wait for each response (Default: 1000).")
    parser.add_argument("-s", "--size", type=int, default=32, help="Buffer size in bytes (Default: 32).")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of requests to be sent (Default: 4).")
    parser.add_argument("-u", "--udp", action="store_true", help="Send ping via UDP.")
    args = parser.parse_args(args)
    
    pyping.ping(args.host, timeout=args.timeout, packet_size=args.size, count=args.count, quiet_output=False, udp=args.udp)

if __name__ == "__main__":
    parse_args()
