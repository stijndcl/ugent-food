from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING

import requests
from dacite import from_dict

from ugent_food.modes.config import Config
from ugent_food.data.entities import DailyMenu
from ugent_food.exceptions import handle_request_error


if TYPE_CHECKING:
    from ugent_food.data.commands import CommandData


__all__ = [
    "mode_menu"
]


def mode_menu(config: Config, data: CommandData):
    """Print the menu for a given date"""
    # Default to current day if nothing supplied
    day = data.date or datetime.now()

    # response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/{day.year}/{day.month}/{day.day}.json")
    response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/2022/4/29.json")

    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()
    menu = from_dict(data_class=DailyMenu, data=response_json)
    menu.print_menu(config)
