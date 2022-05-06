import sys
from datetime import datetime, timedelta
from typing import Optional

from ugent_food.data.commands import Command, CommandData
from ugent_food.data.enums import Language
from ugent_food.modes import Config, mode_config, mode_menu

__all__ = [
    "parse_args"
]


def _get_mode(name: str, argv: list[str]) -> Command:
    modes_mapping = {
        # Avoid circular import, also Config doesn't need itself as an argument
        "config": lambda _, data: mode_config(data.argv)
    }

    if name not in modes_mapping:
        raise NotImplementedError(f"Missing mode from mapping: {name}.")

    return Command(modes_mapping[name], CommandData(argv, datetime.now()))


def _parse_weekday(argument: str, language: Language) -> Optional[datetime]:
    """Parse a specific day of the week
    As the restaurants are closed during the weekends, only monday-friday is supported
    """
    # Specific day of the week, supports EN & NL
    date_args = {
        Language.EN: {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
        },
        Language.NL: {
            "maandag": 0,
            "dinsdag": 1,
            "woensdag": 2,
            "donderdag": 3,
            "vrijdag": 4
        }
    }

    weekday: Optional[int] = None

    for name, _weekday in date_args[language].items():
        if name.startswith(argument):
            weekday = _weekday

    if weekday is None:
        return None

    # Find the next occurrence of [weekday]
    day_dt = datetime.now()

    # Always add at least one - calling [weekday] on that day will show next week
    day_dt += timedelta(days=1)

    while day_dt.weekday() != weekday:
        day_dt += timedelta(days=1)

    return day_dt


def _parse_date_offset(argument: str, language: Language) -> Optional[datetime]:
    """Parse an offset relative to the current day"""
    offsets = {
        Language.EN: {
            "tomorrow": 1,
        },
        Language.NL: {
            "morgen": 1,
            "overmorgen": 2
        }
    }

    offset: Optional[int] = None

    for name, _offset in offsets[language].items():
        if name.startswith(argument):
            offset = _offset

    if offset is None:
        return None

    return datetime.now() + timedelta(days=offset)


def _parse_date(argument: str) -> Optional[datetime]:
    """Parse a DD/MM-date"""
    spl = list(map(int, argument.split("/")))
    day, month = spl[0], spl[1]

    # If no year is given, try to figure it out
    if len(spl) == 2:
        now = datetime.now()
        # If a day has passed already, show next year
        next_year = month < now.month or month == now.month and day < now.day

        spl.append(now.year + (1 if next_year else 0))

    return datetime.strptime(f"{day}/{month}/{spl[2]}", "%-d/%-m/%Y")


# TODO i18n
def parse_args(argv: list[str], config: Config) -> Optional[Command]:
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

    # DD/MM format
    if "/" in first_arg:
        day_dt = _parse_date(first_arg)
        if day_dt is None:
            print(f"Invalid date: {first_arg}")
            return None

    # Try both parsers
    for func in [_parse_weekday, _parse_date_offset]:
        day_dt = func(first_arg, config.translator.language)
        if day_dt is not None:
            break

    # Nothing found
    if day_dt is None:
        print(f"Unable to parse argument: {argv[0]}")
        return None

    return Command(callable=mode_menu, data=CommandData(argv=argv[1:], date=day_dt))
