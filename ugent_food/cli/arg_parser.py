import argparse
import sys
from typing import Optional

from ugent_food.version import __version__

__all__ = [
    "create_parser"
]


class ArgParser(argparse.ArgumentParser):
    """Main argparser to add extra functionality to the built-in one"""
    modes = ["config", "menu"]

    def parse_args(self, args: Optional[list[str]] = None, namespace=None) -> argparse.Namespace:  # type: ignore
        """Overload the default parse_args method to default to the 'menu' subparser,
        allowing cleaner use from the command-line.
        Mypy doesn't seem to enjoy me overloading this though, so an ignore is needed above.
        """
        if args is None:
            args = []

        # Allow triggering modes case-insensitively
        if args and args[0].lower() in self.modes:
            args[0] = args[0].lower()

        try:
            return super().parse_args(args, namespace)
        except argparse.ArgumentError as exc:
            # Error caused by choosing an incorrect mode, which could be
            # passing a day instead of "menu"
            if str(exc).startswith(("invalid choice: ", "unrecognized arguments: ", "argument subparser: ")):
                # Default to the "menu" option
                args = ["menu"] + list(args)

                # Need another try-catch here so we can just print the message instead of raising it again
                # and throwing a massive exception into the user's terminal
                try:
                    # Try parsing the args again, but now with "menu" as the first option
                    return super().parse_args(args, namespace)
                except argparse.ArgumentError:
                    # That wasn't it either, print the ORIGINAL (!) exception out
                    super().error(str(exc))
            else:
                super().error(str(exc))

        return argparse.Namespace()

    def error(self, message: str):
        """Raise an exception instead of printing a message, so we can catch it if we want to"""
        exc = sys.exc_info()[1]
        if exc:
            raise exc

        super().error(message)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argparser, including subparsers for different modules"""
    # Main parser
    parser = ArgParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="ugent-food")
    parser.add_argument("-V", "--version", action="version", version=f"ugent-food {__version__}")

    # Register subparsers
    subparsers = parser.add_subparsers(dest="subparser")

    config_subparser = subparsers.add_parser("config", help="Configure the behaviour of the application.")
    config_subparser.add_argument("subcommand", type=str.lower,
                                  help="The subcommand to execute. ls prints out the current configuration, "
                                       "set allows modifying values. "
                                       "When calling 'set', the 'target' and 'value' arguments are required.",
                                  choices=["ls", "set"])
    config_subparser.add_argument("target", type=str.lower, nargs="?",
                                  help="The name of the setting that should be changed. "
                                       "Only allowed when calling the 'set' subcommand.")
    config_subparser.add_argument("value", type=str.lower, nargs="?",
                                  help="The new value for the chosen setting. "
                                       "Only allowed when calling the 'set' subcommand.")

    menu_subparser = subparsers.add_parser("menu",
                                           help="Commands related to fetching menus. "
                                                "Note that, as this is the most common use-case, "
                                                "it's not required to explicitly add this command. "
                                                "Immediately passing its arguments will work as well "
                                                "(eg. 'ugent_food [day]').")
    menu_subparser.add_argument("day", type=str.lower, nargs="?",
                                help="The day for which to fetch the menu. "
                                     "Defaults to today's menu. "
                                     "This can either be a weekday (eg. 'Monday', 'Tuesday', ...), "
                                     "a date in DD/MM format (eg. 21/09), or a relative offset (eg. 'tomorrow').")

    return parser
