from .ugent_food_exception import UgentFoodException


class ArgumentParsingException(ValueError, UgentFoodException):
    """Raised when something goes wrong while parsing the command-line arguments"""
