from datetime import datetime, timedelta
from typing import Optional

from ugent_food.data.enums import Language

__all__ = [
    "parse_date",
    "parse_date_str",
    "parse_date_offset",
    "parse_weekday"
]


def _find_nearest_match(data: dict[Language, dict[str, int]], argument: str) -> Optional[int]:
    """Find the closest match in a dictionary"""
    for entries in data.values():
        for name, value in entries.items():
            if name.startswith(argument):
                return value

    return None


def parse_weekday(argument: str) -> Optional[datetime]:
    """Parse a specific day of the week
    As the restaurants are closed during the weekends, only Monday-Friday are supported
    """
    # Specific day of the week, supports EN & NL
    weekdays = {
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

    weekday = _find_nearest_match(weekdays, argument)

    if weekday is None:
        return None

    # Find the next occurrence of [weekday]
    day_dt = datetime.now()

    # Always add at least one - calling [weekday] on that day will show next week
    day_dt += timedelta(days=1)

    while day_dt.weekday() != weekday:
        day_dt += timedelta(days=1)

    return day_dt


def parse_date_offset(argument: str) -> Optional[datetime]:
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

    offset = _find_nearest_match(offsets, argument)

    if offset is None:
        return None

    return datetime.now() + timedelta(days=offset)


def parse_date_str(argument: str) -> Optional[datetime]:
    """Parse a DD/MM-date"""
    spl = list(map(int, argument.split("/")))
    day, month = spl[0], spl[1]

    # If no year is given, try to figure it out
    if len(spl) == 2:
        now = datetime.now()
        # If a day has passed already, show next year
        next_year = month < now.month or (month == now.month and day < now.day)

        spl.append(now.year + (1 if next_year else 0))

    return datetime.strptime(f"{day}/{month}/{spl[2]}", "%d/%m/%Y")


def parse_date(argument: str) -> Optional[datetime]:
    """Take a string argument and turn it into a datetime, trying all
    three parsers above (weekday, offset, and DD/MM)
    """
    if "/" in argument:
        return parse_date_str(argument)

    return parse_weekday(argument) or parse_date_offset(argument)
