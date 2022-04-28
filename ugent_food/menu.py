from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Optional, List

import requests
from dacite import from_dict

from ugent_food.data.enums import Message, Kind
from ugent_food.exceptions import handle_request_error
from ugent_food.i18n import Translator


@dataclass
class Meal:
    kind: str
    name: str
    price: str
    type: str

    def __str__(self) -> str:
        return f"- {self.name} ({self.price})"


@dataclass
class Menu:
    open: bool
    meals: list[Meal] = field(default_factory=list)
    message: Optional[str] = None
    vegetables: list[str] = field(default_factory=list)

    def print_menu(self, translator: Translator):
        if not self.open:
            return translator.message(Message.RESTO_CLOSED)

        if soups := self._get_soups():
            soups_str = "\n".join(map(str, soups))
            print(translator.message(Message.SOUP, soup=soups_str))
            print("\n")



    def _get_soups(self) -> Optional[List[Meal]]:
        """Find the soup meal"""
        soups = []

        for meal in self.meals:
            if meal.kind == Kind.SOUP.value:
                soups.append(meal)

        return soups


def menu_for(day: datetime, translator: Translator) -> Menu:
    """Return the menu for a given date"""
    response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{translator.language.value}/{day.year}/{day.month}/{day.day}.json")

    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()

    menu = from_dict(data_class=Menu, data=response_json)

    # print(menu.__dict__)
    menu.print_menu(translator)

    return menu
