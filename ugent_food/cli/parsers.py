from datetime import date, datetime, timedelta
from typing import Optional, Type, Union

__all__ = ["parse_date_argument", "parse_arg_to_type"]


def _forward_date_to(weekday: int, date_instance: date) -> date:
    """Forward a datetime.date until the next occurrence of [weekday]

    This always goes at least one day in the future, so if [date_instance]
    IS already a [weekday], it will go to next week.
    """
    date_instance += timedelta(days=1)
    while date_instance.weekday() != weekday:
        date_instance += timedelta(days=1)

    return date_instance


def parse_date_argument(argument: Optional[str] = None) -> Optional[date]:
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

    # A weekday is passed by name
    weekdays = {
        # English
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
        # Dutch
        "maandag": 0,
        "dinsdag": 1,
        "woensdag": 2,
        "donderdag": 3,
        "vrijdag": 4,
        "zaterdag": 5,
        "zondag": 6,
    }

    for weekday in weekdays:
        if weekday.startswith(argument):
            return _forward_date_to(weekdays[weekday], today)

    # Try various datetime formats
    formats = ["%d/%m", "%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d", "%y-%m-%d", "%m-%d"]
    for _format in formats:
        try:
            dt_instance = datetime.strptime(argument, _format)

            # Configure the year
            if "y" in _format.lower():
                # Explicitly requested the year in the format
                year = dt_instance.year
            elif dt_instance.month < today.month or (dt_instance.month == today.month and dt_instance.day < today.day):
                # Requested a date that has already happened this year
                # Skip to next year, presuming that this is called around NYE (e.g. you're studying in restaurants)
                # There's not much use to calling an old menu, this is more likely
                year = today.year + 1
            else:
                # Default to this year
                year = today.year

            return date(day=dt_instance.day, month=dt_instance.month, year=year)
        except ValueError:
            # This format didn't match, try the next
            continue

    # Can't be parsed
    return None


ARG_TYPES = Union[str, int, bool, list]


def parse_arg_to_type(value: str, type_: Type[ARG_TYPES]) -> ARG_TYPES:
    """Try to parse an argument into type [type]"""
    if type_ == str:
        return value

    if type_ == int:
        return int(value)

    value = value.lower()

    if type_ == bool:
        true_values = ["1", "true", "t", "yes", "y"]
        false_values = ["0", "false", "f", "no", "n"]

        if value in true_values:
            return True

        if value in false_values:
            return False

        raise ValueError

    # For lists: split the list & strip whitespace off
    # This allows adding spaces after arguments if you want to
    if type_ == list:
        return list(map(str.strip, value.split(",")))

    # Could not be parsed
    raise ValueError
