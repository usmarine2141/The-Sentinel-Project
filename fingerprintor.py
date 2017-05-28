from modules import tor
from modules.utils import colored
import argparse, socket, time, sys


__doc__ = "Retrieves descriptor (descriptive) information from hidden service addresses (.onion)."

def parse_args(args: list = sys.argv[1:]):
    Tor = None
    parser = argparse.ArgumentParser("fingerprintor", description=__doc__)
    parser.add_argument("target", type=str, help="Target hidden service address.")
    args = parser.parse_args(args)
    target = args.target
    
    try:
        if not tor.pids():
            print(colored("[i] Tor is actually not running, starting a new temporary instance ...", "yellow"))
            Tor = tor.Tor()
            Tor.start(False, " -  ")
            print("")
        hs = tor.HiddenService(target)
        print(colored("[i] Hidden Service Descriptive Info.:"))
        print(colored(f" -  Publish Date & Time: {hs.published}"))
        print(colored(f" -  Descriptor Identifier: {hs.descriptor_id}"))
        print(colored(f" -  Descriptor Hash: {hs.secret_id_part}"))
        print(colored(f" -  Descriptor Version: {hs.version}"))
        print(colored(f" -  Supported Versions: {', '.join(str(v) for v in hs.protocol_versions)}"))
        print(colored(" -  Permanent Key: "))
        print(colored("    " + hs.permanent_key.replace("\n", "\n    "), dark=True))
        print(colored(" -  Signature: "))
        print(colored("    " + hs.signature.replace("\n", "\n    "), dark=True))
        print(colored(" -  Introduction Points:"))
        print(colored(f"      {' Identifier '.center(32, '-')}  {' Address '.center(21, '-')}"))
        for introduction_point in sorted(hs.introduction_points(), key=lambda x: x.identifier):
            score = status = None
            print(colored(f"    - {introduction_point.identifier}: " + f"{introduction_point.address}:{introduction_point.port}", dark=True))
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
    except KeyboardInterrupt:
        print(colored("[!] Keyboard Interrupted!", "red"))
    if Tor:
        Tor.exit()

if __name__ == "__main__":
    parse_args()
