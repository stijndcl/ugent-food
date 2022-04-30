import sys

from .arg_parser import parse_args
from .data.commands import Command
from .modes import Config


def main(argv=None):
    if argv:
        # Parse the required command out of the argv
        command = parse_args(argv)
    else:
        # Use defaults
        command = Command()

    if command is None:
        print("Unable to parse arguments.", file=sys.stderr)
        exit(1)

    command()
