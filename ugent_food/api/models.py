from dataclasses import dataclass, field

__all__ = ["Menu"]

from enum import Enum
from typing import Optional


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


@dataclass
class Meal:
    """A meal on the menu"""

    kind: MealKind
    name: str
    price: str
    type: MealType


@dataclass
class Menu:
    """Dataclass for a whole menu"""

    open: bool
    meals: list[Meal] = field(default_factory=list)
    vegetables: list[str] = field(default_factory=list)
    message: Optional[str] = None
