from dataclasses import dataclass

from tabulate import tabulate

from ugent_food.data.entities.abc import Menu
from ugent_food.data.enums import Table
from ugent_food.modes.config import Config


@dataclass
class Sandwich:
    """A sandwich with its ingredients"""
    name: str
    price_small: str
    price_medium: str
    ingredients: list[str]

    def __post_init__(self):
        """Add the Euro (€) symbol in front of the prices"""
        if self.price_small:
            self.price_small = f"€{self.price_small}"

        if self.price_medium:
            self.price_medium = f"€{self.price_medium}"


@dataclass
class SandwichMenu(Menu):
    """The menu with all sandwiches"""
    sandwiches: list[Sandwich]

    def __post_init__(self):
        """Sort sandwiches by name"""
        self.sandwiches.sort(key=lambda x: x.name)

    def print_menu(self, config: Config, *args):
        data = []

        for sandwich in self.sandwiches:
            data.append([
                sandwich.name,
                ",".join(sandwich.ingredients),
                sandwich.price_small,
                sandwich.price_medium
            ])

        print(tabulate(data, headers=config.translator.table_headers(Table.SANDWICHES)))
