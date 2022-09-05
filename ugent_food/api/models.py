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
    """The menu for the main dishes available on a given day"""

    open: bool
    meals: list[Meal] = field(default_factory=list)
    vegetables: list[str] = field(default_factory=list)
    message: Optional[str] = None

    _main_kinds_order: list[MealKind] = field(
        init=False,
        default_factory=lambda: [MealKind.MEAT, MealKind.FISH, MealKind.VEGETARIAN, MealKind.VEGAN, MealKind.SOUP],
    )

    def __str__(self) -> str:
        """String representation of a menu: table of all dishes"""
        aggregated = []

        if not self.open:
            aggregated.append("The restaurants are closed.")

        if self.message:
            aggregated.append(self.message)

        return "\n".join(aggregated)
