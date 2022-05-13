import sys
from argparse import Namespace
from datetime import datetime, timedelta
from typing import Optional

from ugent_food.data.api import get_menu, get_sandwiches
from ugent_food.data.entities.abc import Menu
from ugent_food.modes.config import Config
from ugent_food.parsers.dates import parse_date

__all__ = [
    "mode_menu"
]


def get_date(day: Optional[str], config: Config) -> Optional[datetime]:
    """Convert a string argument into a datetime instance"""
    day_dt: datetime

    if day is None:
        # Default to current day if nothing supplied
        day_dt = datetime.now()
    else:
        # Try parsing the requested date out of the argument
        parsed = parse_date(day)
        if parsed is None:
            return None

        day_dt = parsed

    # If the current day is a weekend, and the user doesn't want to see weekends,
    # skip ahead
    if config.skip_weekends:
        while day_dt.weekday() > 4:
            day_dt += timedelta(1)

    return day_dt


def _run_subcommand(config: Config, day_dt: datetime, args: Namespace):
    """Find & run the correct subcommand for the Menu mode"""
    menu: Menu

    if args.get("sandwiches", False):
        menu = get_sandwiches()
    else:
        menu = get_menu(day_dt, config.translator.language)

    menu.print_menu(config, day_dt)


def mode_menu(config: Config, args: Namespace):
    """Print the menu for a given date"""
    day: Optional[str] = args.get("day", None)
    day_dt = get_date(day, config)

    if day_dt is None:
        print(f"Unable to parse argument \"{day}\".", file=sys.stderr)
        sys.exit(1)

    _run_subcommand(config, day_dt, args)
