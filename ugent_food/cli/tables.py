import textwrap

from tabulate import tabulate

from ugent_food.api.models import Sandwich
from ugent_food.i18n import Translator

__all__ = ["sandwich_table"]


def sandwich_table(sandwiches: list[Sandwich], translator: Translator) -> str:
    """Table for the list of sandwiches"""
    table_data = []

    for sandwich in sorted(sandwiches, key=lambda x: x.name):
        ingredients = list(map(str.title, sandwich.ingredients))
        ingredients_str = "".join(textwrap.wrap(", ".join(sorted(ingredients))))

        table_data.append([sandwich.name.title(), ingredients_str, sandwich.price_small, sandwich.price_medium])

    return tabulate(table_data, headers=translator.sandwich_table_headers())
