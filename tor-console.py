import stem.interpreter, colorama, argparse, sys

__doc__ = "Interactive interpreter for interacting with Tor directly."


colorama.init(autoreset=True)

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("tor-console", description=__doc__)
    args = parser.parse_args()
    stem.interpreter.main()

if __name__ == "__main__":
    parse_args()
