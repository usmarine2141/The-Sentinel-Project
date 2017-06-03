import argparse, sys, os
from modules import loader
from modules.utils import colored


__doc__ = "Displays this message."

def list(path):
    location = os.path.abspath(os.path.dirname(__file__))
    for name in sorted(os.listdir(location)):
        path = os.path.join(location, name)
        if not name.startswith("_") and name not in ["modules", "console.py"]:
            #if os.path.isdir(path) and os.path.isfile(os.path.join(path, "__init__.py")):
            #    path = os.path.join(path, "__init__.py")
            
            if os.path.isfile(path) and path.endswith(".py"):
                try:
                    module = loader.load(path)
                    name = name.rsplit(".", 1)[0]
                    doc = module.__doc__.split("\n")[0] or "No description available."
                    if hasattr(module, "parse_args"):
                        print(colored(f" -  {name}: ") + colored(f"{doc}", dark=True))
                except:
                    pass

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("help", description=__doc__)
    args = parser.parse_args(args)
    print(colored("[+] Available Commands:"))
    list("./")

if __name__ == "__main__":
    parse_args()
