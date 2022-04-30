import sys

from .arg_parser import parse_args
from .data.commands import Command
from .modes import Config


def main(argv=None):
    config = Config.load()

    if argv:
        # Parse the required command out of the argv
        command = parse_args(argv, config)
    else:
        # Use defaults
        command = Command()

    # Unable to parse arguments
    if command is None:
        exit(1)

    command(config)
