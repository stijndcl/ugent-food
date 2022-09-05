from .base import UGentFoodException

__all__ = ["APIException"]


class APIException(UGentFoodException):
    """Exception raised when an API request fails"""

    def __init__(self, status_code: int):
        super().__init__(f"API request failed with status code {status_code}.")
