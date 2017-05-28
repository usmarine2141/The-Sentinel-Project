import argparse, sys, os
from modules import loader
from modules.utils import colored


__doc__ = "Displays this message."

def list(path):
    location = os.path.abspath(os.path.dirname(__file__))
    scripts = set()
    for name in sorted(os.listdir(location)):
        if name.lower().endswith(".py"):
            if not name.startswith("_"):
                try:
                    module = loader.load(os.path.join(location, name))
                    name = name.rsplit(".", 1)[0].lower()
                    doc = module.__doc__ or "No description available."
                    if hasattr(module, "parse_args"):
                        print(colored(f" -  {name}: ") + colored(f"{doc}", dark=True))
                except Exception as e:
                    pass

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("help", description=__doc__)
    args = parser.parse_args(args)
    print(colored("[+] Available Commands:"))
    list("./")

if __name__ == "__main__":
    parse_args()
