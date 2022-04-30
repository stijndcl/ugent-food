import sys

from .arg_parser import parse_args
from .modes import Config


def main(argv=None):
    # Parse the required command out of the argv
    command = parse_args(argv)

    if command is None:
        print("Unable to parse arguments.", file=sys.stderr)
        exit(1)

    command()
