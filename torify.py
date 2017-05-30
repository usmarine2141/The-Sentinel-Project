import argparse, sys, os
from modules.socket import proxify
from modules import loader


__doc__ = "Proxy scripts through Tor ..."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("proxify", description=__doc__, prefix_chars="/")
    parser.add_argument("script", type=str, help="Target script.")
    parser.add_argument("arguments", nargs="+", metavar="Argument", default=[], help="Arguments.")
    args = parser.parse_args(args)
    
    module = loader.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), args.script + ("" if args.script.endswith(".py") else ".py")))
    proxify("127.0.0.1", 9150)
    module.parse_args(args.arguments)

if __name__ == "__main__":
    parse_args()
