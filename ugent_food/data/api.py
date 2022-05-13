from datetime import datetime
from http import HTTPStatus
from typing import Type, TypeVar, Optional

import requests
from dacite import from_dict

from ..data.entities import DailyMenu, SandwichMenu
from ..data.enums import Language
from ..exceptions import handle_request_error
from ..version import __version__

__all__ = [
    "get_menu",
]

headers = {
    "User-Agent": f"ugent-food (v{__version__})"
}


T = TypeVar("T")


def _do_api_call(endpoint: str, class_: Type[T], wrap_in: Optional[str] = None, **kwargs) -> T:
    """Perform an API call & convert to a dataclass"""
    url_base = "https://hydra.ugent.be/api/2.0/resto"
    response = requests.get(url_base + endpoint, headers)

    if response.status_code != HTTPStatus.OK:
        handle_request_error(response.status_code, **kwargs)

    response_json = response.json()

    # Wrap the response in a dict in case it isn't
    if wrap_in is not None:
        response_json = {wrap_in: response_json}

    return from_dict(data_class=class_, data=response_json)


def get_menu(day: datetime, language: Language) -> DailyMenu:
    """Get the menu for a given day"""
    url = f"/menu/{language.value}/{day.year}/{day.month}/{day.day}.json"
    return _do_api_call(url, DailyMenu, day=day)


def get_sandwiches() -> SandwichMenu:
    """Get all available sandwiches"""
    url = "/sandwiches/static.json"
    return _do_api_call(url, SandwichMenu, wrap_in="sandwiches")
