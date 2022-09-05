from datetime import date
from http import HTTPStatus

from aiohttp import ClientSession
from dacite import from_dict

from ugent_food.api.models import Menu
from ugent_food.exceptions import APIException
from ugent_food.version import __version__

__all__ = ["fetch_menu"]

headers = {"User-Agent": f"ugent-food (v{__version__})"}


async def fetch_menu(client_session: ClientSession, day: date, language: str) -> Menu:
    """Get the menu for a given day"""
    endpoint = f"https://hydra.ugent.be/api/2.0/resto/menu/{language}/{day.year}/{day.month}/{day.day}.json"
    async with client_session.get(endpoint, headers=headers) as response:
        if response.status != HTTPStatus.OK:
            raise APIException(response.status)

        data = await response.json()
        return from_dict(Menu, data)
