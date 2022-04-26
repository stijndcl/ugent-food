import sys
from argparse import Namespace
from datetime import datetime, timedelta
from typing import Optional

from ugent_food.data.api import get_menu
from ugent_food.modes.config import Config
from ugent_food.parsers.dates import parse_date

__all__ = [
    "mode_menu"
]


def mode_menu(config: Config, args: Namespace):
    """Print the menu for a given date"""
    day: Optional[str] = args.get("day", None)
    day_dt: datetime

    if day is None:
        # Default to current day if nothing supplied
        day_dt = datetime.now()
    else:
        # Try parsing the requested date out of the argument
        parsed = parse_date(day)
        if parsed is None:
            print(f"Unable to parse argument \"{day}\".", file=sys.stderr)
            sys.exit(1)

        day_dt = parsed

    # If the current day is a weekend, and the user doesn't want to see weekends,
    # skip it
    if config.skip_weekends:
        while day_dt.weekday() > 4:
            day_dt += timedelta(1)

    menu = get_menu(day_dt, config.translator.language)
    menu.print_menu(config, day_dt)
