from enum import Enum

__all__ = ["MealKind", "MealType"]


class MealKind(str, Enum):
    """Enum for the different kinds of meals"""

    FISH = "fish"
    MEAT = "meat"
    SOUP = "soup"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"


class MealType(str, Enum):
    """Enum for the different categories of meals"""

    COLD = "cold"
    MAIN = "main"
    SIDE = "side"
