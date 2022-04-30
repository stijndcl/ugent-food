import sys
from datetime import datetime
from typing import Optional

from ugent_food.data.commands import Command, CommandData
from ugent_food import modes


__all__ = [
    "parse_args"
]

from ugent_food.modes import mode_menu


def _get_mode(name: str, argv: list[str]) -> Command:
    modes_mapping = {
        # Avoid circular import, also Config doesn't need itself as an argument
        "config": lambda _, command: modes.mode_config(command.data.argv)
    }

    if name not in modes_mapping:
        raise NotImplementedError(f"Missing mode from mapping: {name}.")

    return Command(modes_mapping[name], CommandData(argv, datetime.now()))


def _parse_weekday(argument: str) -> Optional[datetime]:
    """Parse a specific weekday"""
    # Specific day of the week
    date_args = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "maandag": 0,
        "dinsdag": 1,
        "woensdag": 2,
        "donderdag": 3,
        "vrijdag": 4
    }

    for date in date_args:
        if date.startswith(argument):
            # TODO
            print(f"Detected date: {date}")
            exit(0)

    return None


def _parse_date_offset(argument: str) -> Optional[datetime]:
    """Parse an offset relative to the current day"""
    offsets = {
        "tomorrow": 1,
        "morgen": 1,
        "overmorgen": 2
    }

    return None


def _parse_date(argument: str) -> Optional[datetime]:
    """Parse a DD/MM-date"""
    # TODO

    return None


def parse_args(argv: list[str]) -> Optional[Command]:
    """Argparser
    As the package supports passing the target date as the first argument,
    as well as multiple modes, this isn't really doable using the built-in
    argparse package
    """
    first_arg = argv[0].lower()

    modes = [
        "config",
    ]

    # Trying to call a mode
    if first_arg in modes:
        return _get_mode(first_arg, argv[1:])

    # Require at least two characters to parse a date
    if len(first_arg) < 2:
        print("Argument too short (length must be at least 2).", file=sys.stderr)
        return None

    day_dt: Optional[datetime] = None

    # DD/MM format
    if "/" in first_arg:
        day_dt = _parse_date(first_arg)
        if day_dt is None:
            print(f"Invalid date: {first_arg}")
            return None

    # Try both parsers
    for func in [_parse_weekday, _parse_date_offset]:
        day_dt = func(first_arg)
        if day_dt is not None:
            break

    # Nothing found
    if day_dt is None:
        print(f"Unable to parse argument: {argv[0]}")
        return None

    return Command(callable=mode_menu, data=CommandData(argv=argv[1:], date=day_dt))
