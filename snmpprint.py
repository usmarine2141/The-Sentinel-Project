from pysnmp.hlapi import *
from modules.utils import *
import argparse, netaddr, time, sys


def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("snmpprint", description=__doc__)
    parser.add_argument("-t", "--target", type=str, help="Target address or hostname.")
    parser.add_argument("-p", "--port", type=int, default=161, help="Target SNMP port.")
    parser.add_argument("-l", "--list", type=argparse.FileType("r"), help="Target list.")
    parser.add_argument("-c", "--community", type=str, default="public", help="Community name.")
    parser.add_argument("-g", "--get", nargs="+", type=str, help="Use getCmd for the object identities specified here against the target(s) instead of using nextCmd.")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Response timeout in seconds.")
    parser.add_argument("-r", "--retries", type=int, default=5, help="Maximum number of request retries, 0 retries means just a single request.")
    parser.add_argument("-6", "--udp6", action="store_true", help="Use the UDP6 Transport.")
    parser.add_argument("-u", "--unix", action="store_true", help="Use the Unix Transport.")
    args = parser.parse_args(args)
    try:
        targets = []
        if args.target:
            targets.append(netaddr.IPAddress(args.target))
        if args.list:
            data = chunk = args.list.read(0xFFF)
            while chunk:
                chunk = args.list.read(0xFFF)
                data += chunk
            for line in data.split("\n"):
                line = line.strip()
                if line:
                    try:
                        targets.append(netaddr.IPAddress(line))
                    except:
                        pass
        targets = sorted(set(targets))
        print(colored(f"[i] {len(targets) or 'No'} target{'s' if len(targets) != 1 else ''} loaded!"))
        if targets:
            transport = Udp6TransportTarget if args.udp6 else (UnixTransportTarget if args.unix else UdpTransportTarget)
            print(colored(f"[i] Starting SNMPPrint at {time.ctime()} ({time.tzname[0]})."))
            print(colored(f" -  Transport: {transport.__name__}", dark=True))
            print(colored(f" -  Timeout: {args.timeout}", dark=True))
            print(colored(f" -  Max Retries: {args.retries}", dark=True))
            print(colored(f" -  Community: {args.community}", dark=True))
            print("")
            for target in targets:
                try:
                    t_str = f"[+] {target}: "
                    print(colored(t_str), end="")
                    if args.get:
                        response = next(getCmd(SnmpEngine(),
                                               CommunityData(args.community, mpModel=0),
                                               transport((str(target), args.port), timeout=args.timeout, retries=args.retries),
                                               ContextData(),
                                               *[ObjectType(ObjectIdentity(obj)) for obj in args.get]))[-1]
                        if response:
                            for value in response:
                                print(colored(f"{' ' * len(t_str) if response.index(value) != 0 else ''}{value.prettyPrint()}", dark=True))
                        else:
                            print(colored("No response ...", "yellow", True))
                    else:
                        generator = nextCmd(SnmpEngine(),
                                            CommunityData(args.community, mpModel=0),
                                            transport((str(target), args.port), timeout=args.timeout, retries=args.retries),
                                            ContextData(),
                                            ObjectType(ObjectIdentity("SNMPv2-MIB")))
                        record = next(generator, None)
                        print("")
                        while record:
                            for value in record[-1]:
                                print(colored(f" -  {value.prettyPrint()}"))
                            record = next(generator, None)
                except Exception as e:
                    print(colored(f"{e}", "red", True))
    except Exception as e:
        print("\n", colored(f"[!] {type(e).__name__}{':' if str(e) else ''}", "red"))
        if str(e):
            print(colored(f" -  {e}", "red", True))


if __name__ == "__main__":
    parse_args()
