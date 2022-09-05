from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from ugent_food.api.enums import MealKind, MealType
from ugent_food.cli.config import Config
from ugent_food.i18n import Message

__all__ = ["Menu"]


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

    def to_string(self, config: Config, day: date) -> str:
        """String representation of a menu: table of all dishes"""
        aggregated = []

        if not self.open:
            aggregated.append(config.translator.message(Message.RESTO_CLOSED, day=day))

        # Remove hidden meals
        acceptable_kinds = list(filter(lambda x: x not in config.hidden, self._main_kinds_order))
        self.meals = list(filter(lambda _meal: _meal.kind in acceptable_kinds, self.meals))

        if self.message:
            aggregated.append(self.message)

        return "\n".join(aggregated)
