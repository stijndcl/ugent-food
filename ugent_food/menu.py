from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Optional

import requests
from dacite import from_dict

from ugent_food.config import Config
from ugent_food.data.enums import Message, Kind, Type
from ugent_food.exceptions import handle_request_error


@dataclass
class Meal:
    kind: str
    name: str
    price: str
    type: str

    def __str__(self) -> str:
        value = ""

        if self.type != Type.SIDE.value:
            value = "  "

        value += f"  ⌞ {self.name}"

        if self.price:
            value += f" ({self.price})"

        return value


@dataclass
class Menu:
    open: bool
    meals: list[Meal] = field(default_factory=list)
    message: Optional[str] = None
    vegetables: list[str] = field(default_factory=list)
    _main_kinds_order: list[Kind] = field(init=False, default_factory=lambda: [
        Kind.MEAT, Kind.FISH, Kind.VEGETARIAN, Kind.VEGAN
    ])

    def print_menu(self, config: Config):
        """Format & print the entire menu to console"""
        translator = config.translator

        if not self.open:
            return translator.message(Message.RESTO_CLOSED)

        if soups := self._get_soups():
            soups_str = "\n".join(map(str, soups))
            print(translator.message(Message.SOUP, soup=soups_str))

        if (main_courses := self._get_main_courses()).keys():
            mains = []

            for kind in self._main_kinds_order:
                if kind not in main_courses:
                    continue

                mains.append(f"  ⌞ {translator.kind(kind)}")

                for meal in main_courses[kind]:
                    mains.append(str(meal))

            mains_str = "\n".join(map(str, mains))
            print(translator.message(Message.MAIN_COURSES, main=mains_str))

        if self.vegetables:
            vegetables_str = "\n".join(map(lambda x: f"  ⌞ {x}", self.vegetables))
            print(translator.message(Message.VEGETABLES, vegetables=vegetables_str))

    def _get_soups(self) -> list[Meal]:
        """Find the soup meals"""
        soups = []

        for meal in self.meals:
            if meal.kind == Kind.SOUP.value:
                soups.append(meal)

        return soups

    def _get_main_courses(self) -> defaultdict[Kind, list[Meal]]:
        """Find the main courses"""
        mains = defaultdict(list)

        mains_filtered = filter(lambda x: x.type == Type.COLD.value, self.meals)

        # Get all meals in order of kind
        for kind in self._main_kinds_order:
            for meal in filter(lambda x: x.kind == kind.value, mains_filtered):
                mains[kind].append(meal)

        return mains


def menu_for(day: datetime, config: Config) -> Menu:
    """Return the menu for a given date"""
    response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/{day.year}/{day.month}/{day.day}.json")

    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()

    menu = from_dict(data_class=Menu, data=response_json)

    # print(menu.__dict__)
    menu.print_menu(config)

    return menu
