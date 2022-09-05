from datetime import date, timedelta
from typing import Optional

__all__ = ["parse_date_argument"]


def parse_date_argument(argument: Optional[str] = None, *, skip_weekends: bool) -> Optional[date]:
    """Try to parse an argument into a date"""
    today = date.today()

    # Default to today
    if argument is None:
        return today

    argument = argument.lower()

    # Explicitly request today
    # No idea why you would do this, but you can
    if argument in (
        "today",
        "vandaag",
    ):
        return today

    # Relative offset
    relative_offsets = {
        "tomorrow": 1,
        "morgen": 1,
        "overmorgen": 2,
    }

    if argument in relative_offsets:
        return today + timedelta(relative_offsets[argument])

    # Can't be parsed
    return None
