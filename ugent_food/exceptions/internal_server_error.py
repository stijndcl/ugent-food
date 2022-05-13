from .ugent_food_exception import UgentFoodException


class InternalServerError(RuntimeError, UgentFoodException):
    """Raised when we can't contact the server"""
    def __init__(self, status_code: int):
        super().__init__(f"Internal server error (status {status_code}).")
