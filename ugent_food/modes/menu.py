from datetime import datetime
from http import HTTPStatus

import requests
from dacite import from_dict

from ugent_food.data.utils import headers
from ugent_food.modes.config import Config
from ugent_food.data.entities import DailyMenu
from ugent_food.exceptions import handle_request_error


__all__ = [
    "mode_menu"
]


def mode_menu(config: Config, args: dict):
    """Print the menu for a given date"""
    # Default to current day if nothing supplied
    day = args.get("day", None) or datetime.now()

    response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/{day.year}/{day.month}/{day.day}.json", headers=headers)

    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()
    menu = from_dict(data_class=DailyMenu, data=response_json)
    menu.print_menu(config, day)
