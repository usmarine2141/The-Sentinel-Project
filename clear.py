import argparse, sys


__doc__ = "Clears the screen."

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("clear", description=__doc__)
    args = parser.parse_args(args)
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
