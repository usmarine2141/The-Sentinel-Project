import argparse, netaddr, sys
from modules.utils import colored


__doc__ = """IEEE EUI (Extended Unique Identifier) lookup tool.
Both EUI-48 (used for layer 2 MAC addresses) and EUI-64 are supported.

Input parsing for EUI-48 addresses is flexible, supporting many MAC
variants."""

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("help", description=__doc__)
    parser.add_argument("address", type=str, metavar="MAC Address", help="Target MAC Address.")
    args = parser.parse_args(args)

    address = int(args.address) if args.address.isdigit() else args.address
    try:
        mac = netaddr.EUI(address)
        info = mac.info["OUI"]
        
        print(colored(f"[i] Media Access Control Address Lookup For {mac}:"))
        print(colored(f" -  Extended Unique Identifier 64:       {mac.eui64()}", dark=True))
        print(colored(f" -  Modified EUI64 Address:              {mac.modified_eui64()}", dark=True))
        print(colored(f" -  Individual Access Block [IAB]:       {mac.iab if mac.is_iab() else 'Not an IAB'}", dark=True))
        print(colored(f" -  Organizationally Unique Identifier:  {mac.oui}", dark=True))
        print(colored(f" -  Extended Identifier [EI]:            {mac.ei}", dark=True))
        print(colored(f" -  Local Link IPv6 Address:             {mac.ipv6_link_local()}", dark=True))
        print(colored(f" -  Vendor Info:"))
        print(colored(f"    - Organization: {info['org']}", dark=True))
        print(colored( "    - Address:      {}".format("\n                    ".join(info["address"])), dark=True))
        print(colored(f" -  OUI Info:"))
        print(colored(f"    - Version: {mac.version}", dark=True))
        print(colored(f"    - Offset:  {info['offset']}", dark=True))
        print(colored(f"    - Size:    {info['size']}", dark=True))
        print(colored(f"    - IDX:     {info['idx']}", dark=True))
        print(colored(f"    - OUI:     {info['oui']}", dark=True))
        print(colored(f" -  Packed Address:          {mac.packed}", dark=True))
        print(colored(f" -  Hexadecimal Address:     {hex(mac)}", dark=True))
        print(colored(f" -  48-bit Positive Integer: {mac.value}", dark=True))
        print(colored(f" -  Octets:                  {', '.join(str(n) for n in mac.words)}", dark=True))
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
