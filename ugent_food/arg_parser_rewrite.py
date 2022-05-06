import argparse


__all__ = [
    "create_parser"
]

import sys
from typing import Optional


class ArgParser(argparse.ArgumentParser):
    def parse_args(self, args: Optional[list[str]] = None) -> argparse.Namespace:  # type: ignore
        """Overload the main parse_args method to default to the 'menu' subparser,
        allowing cleaner use from the command-line.
        Mypy doesn't seem to enjoy me overloading this though, so an ignore is needed above.
        """
        if args is None:
            args = []

        # Make parser case-insensitive
        args = list(map(lambda x: x.lower(), args))

        try:
            return super().parse_args(args)
        except argparse.ArgumentError as exc:
            # Error caused by choosing an incorrect mode, which could be
            # passing a day instead of "menu"
            if str(exc).startswith(("invalid choice: ", "unrecognized arguments: ")):
                # Default to the "menu" option
                args = ["menu"] + list(args)

                # Need another try-catch here so we can just print the message instead of raising it again
                # and throwing a massive exception into the user's terminal
                try:
                    # Try parsing the args again, but now with "menu" as the first option
                    print(args)
                    return super().parse_args(args)
                except argparse.ArgumentError as new_exc:
                    print(str(new_exc))
                    # That wasn't it either, print the ORIGINAL (!) exception out
                    super().error(str(exc))
            else:
                super().error(str(exc))

    def error(self, message: str):
        exc = sys.exc_info()[1]
        if exc:
            raise exc

        super().error(message)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argparser, including subparsers for different modules"""
    # Main parser
    parser = ArgParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="ugent-food")
    subparsers = parser.add_subparsers()

    config_subparser = subparsers.add_parser("config", help="Configure the behaviour of the application.")
    config_subparser.add_argument("action", help="The action to perform.", choices=["ls", "set"])

    menu_subparser = subparsers.add_parser("menu", help="Commands related to fetching the menu.")
    menu_subparser.add_argument("day", nargs="?", help="The day for which to fetch the menu. Defaults to today's menu. This can either be a weekday (eg. 'monday', 'tuesday', ...), a date in DD/MM format (eg. 21/09), or a relative offset (eg. 'tomorrow').")
    menu_subparser.add_argument("-S", "--sandwiches", action="store_true", help="Show the available sandwiches instead of the usual meals.")

    return parser
