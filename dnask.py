import dns.resolver, dns.message, socket, random, argparse, sys
from modules.utils import *


__doc__ = "Utility to build and execute DNS queries ..."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("dnask", description=__doc__)
    parser.add_argument("query", type=str, metavar="STRING", help="Query string.")
    parser.add_argument("-t", "--rdtype", type=str, default=1, help="Query type.")
    parser.add_argument("-c", "--rdclass", type=str, default=1, help="Query class.")
    parser.add_argument("-s", "--source", type=str, default=socket.gethostbyname(socket.gethostname()), help="Source address.")
    parser.add_argument("-sP", "--source-port", type=int, default=random.randint(1, 65535), help="Source port.")
    parser.add_argument("--tcp", action="store_true", help="Use TCP to make the query.")
    parser.add_argument("-ns", "--nameservers", nargs="+", type=str, metavar="NAMESERVER", help="A list of nameservers to query. Each nameserver is a string which contains the IP address of a nameserver.")
    parser.add_argument("-p", "--port", type=int, default=53, help="The port to which to send queries (Defaults to 53).")
    parser.add_argument("-T", "--timeout", type=int, default=8, help="The number of seconds to wait for a response from a server, before timing out.")
    parser.add_argument("-l", "--lifetime", type=int, default=8, help="The total number of seconds to spend trying to get an answer to the question. If the lifetime expires, a Timeout exception will occur.")
    parser.add_argument("-e", "--edns", type=int, default=-1, help="The EDNS level to use (Defaults to -1, no Edns).")
    parser.add_argument("-eF", "--edns-flags", type=int, help="The EDNS flags.")
    parser.add_argument("-eP", "--edns-payload", type=int, default=0, help="The EDNS payload size (Defaults to 0).")
    parser.add_argument("-f", "--flags", type=int, default=None, help="The message flags to use (Defaults to None (i.e. not overwritten)).")
    parser.add_argument("-r", "--retry-servfail", action="store_true", help="Retry a nameserver if it says SERVFAIL.")
    parser.add_argument("--filename", type=argparse.FileType("r"), help="The filename of a configuration file in standard /etc/resolv.conf format. This parameter is meaningful only when I{configure} is true and the platform is POSIX.")
    parser.add_argument("--configure-resolver", action="store_false", help="If True (the default), the resolver instance is configured in the normal fashion for the operating system the resolver is running on. (I.e. a /etc/resolv.conf file on POSIX systems and from the registry on Windows systems.")
    args = parser.parse_args(args).__dict__
    nameservers = args.pop("nameservers")
    
    resolver = dns.resolver.Resolver(args.pop("filename"), args.pop("configure_resolver"))
    resolver.set_flags(args.pop("flags"))
    resolver.use_edns(args.pop("edns"), args.pop("edns_flags"), args.pop("edns_payload"))
    if nameservers:
        resolver.nameservers = nameservers
    resolver.port = args.pop("port")
    resolver.timeout = args.pop("timeout")
    resolver.lifetime = args.pop("lifetime")
    resolver.retry_servfail = args.pop("retry_servfail")
    answer = resolver.query(args.pop("query"), **args)
    print(colored(answer.response, dark=True))

if __name__ == "__main__":
    try:
        parse_args()
    except (Exception, KeyboardInterrupt) as e:
        print(colored(f"[!] {type(e).__name__}" + (":" if e else ""), "red"))
        if e:
            print(colored(f" -  {e}", "red", True))
