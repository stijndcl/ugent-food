import abc
import sys
from dataclasses import field, dataclass
from datetime import datetime
from typing import Optional

from tabulate import tabulate

from ..modes.config import Config
from .enums import Kind, Type, Message


@dataclass
class Meal:
    """Class to store data for a meal on the menu"""
    name: str
    kind: str
    price: str
    type: str


@dataclass
class MenuMixin:
    """Mixin class to make Mypy happy"""


class Menu(abc.ABC, MenuMixin):
    """Abstract class for menu's"""

    @abc.abstractmethod
    def print_menu(self, config: Config, date: datetime):
        """Abstract method that all Menu's should implement
        Print the menu to the terminal
        """
        raise NotImplementedError


@dataclass
class DailyMenu(Menu):
    """The menu for the main dishes available on a given day"""
    open: bool
    meals: list[Meal] = field(default_factory=list)
    message: Optional[str] = None
    vegetables: list[str] = field(default_factory=list)
    _main_kinds_order: list[Kind] = field(init=False, default_factory=lambda: [
        Kind.MEAT, Kind.FISH, Kind.VEGETARIAN, Kind.VEGAN, Kind.SOUP
    ])

    def print_menu(self, config: Config, date: datetime):
        """Format & print the entire menu to console"""
        translator = config.translator

        table_data = []

        if not self.open:
            print(translator.message(Message.RESTO_CLOSED))
            sys.exit(0)

        # Group by type
        for _type in [Type.MAIN, Type.SIDE, Type.COLD]:
            meals = self._get_meals_by_type(_type)

            for meal in meals:
                # Translate to emoji's or preferred language
                meal_data = [
                    translator.type(Type.from_str(meal.type)),
                    translator.kind(Kind.from_str(meal.kind)),
                    meal.name,
                    meal.price
                ]

                table_data.append(meal_data)

        weekday = translator.weekday(date.weekday())
        day = date.strftime('%d/%m/%Y')
        print(translator.message(Message.MENU_FOR, day=day, weekday=weekday) + "\n")
        print(tabulate(table_data, headers=["Type", "Kind", "Name", "Price"]))

        if self.vegetables:
            vegetables_str = "\n".join(map(lambda x: f"- {x}", self.vegetables))
            print("\n" + translator.message(Message.VEGETABLES, vegetables=vegetables_str))

    def _get_meals_by_type(self, _type: Type) -> list[Meal]:
        """Get all meals of a given type"""
        meals = []
        type_meals = list(filter(lambda x: x.type == _type.value, self.meals))

        # Group by kind
        for kind in self._main_kinds_order:
            # Don't use filter() here because the argument of the lambda
            # is defined in a loop (unsafe)
            for meal in type_meals:
                if meal.kind == kind.value:
                    meals.append(meal)

        return meals
