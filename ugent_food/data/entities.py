import abc
from dataclasses import field, dataclass
from typing import Optional

from tabulate import tabulate

from ugent_food import Config
from ugent_food.data.enums import Kind, Type, Message


@dataclass
class Meal:
    name: str
    kind: str
    price: str
    type: str

    def __iter__(self):
        """Override the __iter__ method to allow list(Meal)"""
        yield self.type
        yield self.kind
        yield self.name
        yield self.price


@dataclass
class Menu(abc.ABC):
    """Abstract class for menu's"""

    @abc.abstractmethod
    def print_menu(self, config: Config):
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

    def print_menu(self, config: Config):
        """Format & print the entire menu to console"""
        translator = config.translator

        table_data = []

        if not self.open:
            return translator.message(Message.RESTO_CLOSED)

        # Group by type
        for _type in [Type.MAIN, Type.SIDE, Type.COLD]:
            meals = self._get_meals_by_type(_type)

            for meal in meals:
                table_data.append(list(meal))

        # TODO translations
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
            for meal in filter(lambda x: x.kind == kind.value, type_meals):
                meals.append(meal)

        return meals
