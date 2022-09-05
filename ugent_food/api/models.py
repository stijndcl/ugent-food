from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from tabulate import tabulate

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

    def _get_meals_by_type(self, meal_type: MealType) -> list[Meal]:
        """Get all meals of a given type"""
        return list(filter(lambda _meal: _meal.type == meal_type, self.meals))

    def to_string(self, config: Config, day: date) -> str:
        """String representation of a menu: table of all dishes"""
        aggregated = []

        if not self.open:
            aggregated.append(config.translator.message(Message.RESTO_CLOSED, day=day))

        table_data: list[list[str]] = []

        # Remove hidden meals
        acceptable_kinds = list(filter(lambda x: x not in config.hidden, self._main_kinds_order))
        self.meals = list(filter(lambda _meal: _meal.kind in acceptable_kinds, self.meals))

        for _type in [MealType.MAIN, MealType.SIDE, MealType.COLD]:
            meals = self._get_meals_by_type(_type)

            for meal in meals:
                meal_data = [
                    config.translator.type(meal.type),
                    config.translator.kind(meal.kind),
                    meal.name,
                    meal.price,
                ]

                table_data.append(meal_data)

        # Menu header
        weekday = config.translator.weekday(day.weekday())
        day_str = day.strftime("%d/%m/%Y")

        # Create table
        aggregated.append(config.translator.message(Message.MENU_FOR, day=day_str, weekday=weekday))
        aggregated.append("\n" + tabulate(table_data, headers=config.translator.table_headers()))

        if self.vegetables:
            vegetables_str = "\n".join(map(lambda x: f"- {x}", self.vegetables))
            aggregated.append("\n" + config.translator.message(Message.VEGETABLES, vegetables=vegetables_str))

        if self.message:
            aggregated.append("\n" + config.translator.message(Message.EXTRA_MESSAGE, extra=self.message))

        return "\n".join(aggregated)
