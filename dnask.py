import dns.resolver, dns.message, socket, random, argparse, sys
from modules.utils import *


__doc__ = "Utility to build and execute DNS queries ..."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("dnask", description=__doc__)
    parser.add_argument("query", type=str, metavar="STRING", help="Query string.")
    parser.add_argument("-t", "--rdtype", type=str, default=1, help="Query type.")
    parser.add_argument("-c", "--rdclass", type=str, default=1, help="Query class.")
    parser.add_argument("-m", "--metaquery", action="store_true", help="Execute as MetaQuery.")
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
    parser.add_argument("-S", "--want-dnssec", action="store_true", help="Indicate that DNSSEC is desired.")
    parser.add_argument("-f", "--flags", type=int, default=None, help="The message flags to use (Defaults to None (i.e. not overwritten)).")
    parser.add_argument("-r", "--retry-servfail", action="store_true", help="Retry a nameserver if it says SERVFAIL.")
    parser.add_argument("-R", "--one-rr-per-rrset", action="store_true", help="Put each RR into its own RRset (Only useful when executing MetaQueries).")
    parser.add_argument("--filename", type=argparse.FileType("r"), help="The filename of a configuration file in standard /etc/resolv.conf format. This parameter is meaningful only when I{configure} is true and the platform is POSIX.")
    parser.add_argument("--configure-resolver", action="store_false", help="If True (the default), the resolver instance is configured in the normal fashion for the operating system the resolver is running on. (I.e. a /etc/resolv.conf file on POSIX systems and from the registry on Windows systems.")
    args = parser.parse_args(args).__dict__
    nameservers = args.get("nameservers")
    
    resolver = dns.resolver.Resolver(args.get("filename"), args.get("configure_resolver"))
    resolver.set_flags(args.get("flags"))
    resolver.use_edns(args.get("edns"), args.get("edns_flags"), args.get("edns_payload"))
    if not nameservers:
        nameservers = resolver.nameservers
    resolver.nameservers = nameservers
    resolver.port = args.get("port")
    resolver.timeout = args.get("timeout")
    resolver.lifetime = args.get("lifetime")
    resolver.retry_servfail = args.get("retry_servfail")
    if args.pop("metaquery"):
        kwargs = {v: args.get(k) for k, v in {"rdclass": "rdclass", "edns": "use_edns", "want_dnssec": "want_dnssec", "edns_flags": "ednsflags", "edns_payload": "request_payload"}.items()}
        message = dns.message.make_query(args.get("query"), args.get("rdtype"), **kwargs)
        kwargs = {k: args.get(k) for k in ["timeout", "port", "source", "source_port", "one_rr_per_rrset"]}
        if args.get("tcp"):
            resp = dns.query.tcp(message, nameservers[0], **kwargs)
        else:
            resp = dns.query.udp(message, nameservers[0], **kwargs)
        print(colored(resp))
    else:
        kwargs = {k: args.get(k) for k in ["rdtype", "rdclass", "tcp", "source", "source_port"]}
        answer = resolver.query(args.pop("query"), **kwargs)
        print(colored(answer.response))

if __name__ == "__main__":
    try:
        parse_args()
    except (Exception, KeyboardInterrupt) as e:
        print(colored(f"[!] {type(e).__name__}" + (":" if e else ""), "red"))
        if e:
            print(colored(f" -  {e}", "red", True))
