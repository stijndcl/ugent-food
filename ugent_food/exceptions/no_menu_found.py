from datetime import datetime


class NoMenuFoundException(ValueError):
    """Exception raised when no menu could be found"""
    def __init__(self, date: datetime):
        super().__init__(f"No menu could be found for {date.day:02d}/{date.month:02d}/{date.year}.")
