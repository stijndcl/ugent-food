from .base import UGentFoodException

__all__ = ["NoMenuFound"]


class NoMenuFound(UGentFoodException):
    """Exception raised when no menu could be found"""
