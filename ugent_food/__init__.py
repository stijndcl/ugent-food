from typing import Callable

from ugent_food.cli.arg_parser import create_parser
from .modes import Config, mode_config, mode_menu


def main(argv=None):
    config = Config.load()

    # Parse command line arguments
    args_namespace = vars(create_parser().parse_args(argv))

    # Set menu as the default subparser
    if args_namespace.get("subparser", None) is None:
        args_namespace["subparser"] = "menu"

    # Link mode names to methods
    modes_mapping: dict[str, Callable[[Config, dict], None]] = {
        "config": mode_config,
        "menu": mode_menu
    }

    # Run the requested mode
    modes_mapping[args_namespace.get("subparser")](config, args_namespace)
