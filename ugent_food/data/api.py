from datetime import datetime
from http import HTTPStatus

import requests
from dacite import from_dict

from ..data.entities import DailyMenu
from ..data.enums import Language
from ..exceptions import handle_request_error
from ..version import __version__

__all__ = [
    "get_menu",
]

headers = {
    "User-Agent": f"ugent-food (v{__version__})"
}


def get_menu(day: datetime, language: Language) -> DailyMenu:
    """Get the menu for a given day"""
    url = f"https://hydra.ugent.be/api/2.0/resto/menu/{language.value}/{day.year}/{day.month}/{day.day}.json"
    response = requests.get(url, headers=headers)

    # Something went wrong, raise an exception
    if response != HTTPStatus.OK:
        handle_request_error(response.status_code, day)

    response_json = response.json()
    return from_dict(data_class=DailyMenu, data=response_json)
