from datetime import datetime
from http import HTTPStatus

import requests
from dacite import from_dict

from ugent_food.config import Config
from ugent_food.data.entities import Menu, DailyMenu
from ugent_food.exceptions import handle_request_error


def menu_for(day: datetime, config: Config) -> Menu:
    """Return the menu for a given date"""
    # response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/{day.year}/{day.month}/{day.day}.json")
    response = requests.get(f"https://hydra.ugent.be/api/2.0/resto/menu/{config.translator.language.value}/2022/4/29.json")

    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()
    menu = from_dict(data_class=DailyMenu, data=response_json)

    return menu
