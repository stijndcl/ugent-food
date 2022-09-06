from datetime import date
from enum import Enum
from http import HTTPStatus

from aiohttp import ClientSession
from dacite import Config, from_dict

from ugent_food.api.models import Menu, Sandwich
from ugent_food.exceptions import APIException, NoMenuFound
from ugent_food.version import __version__

__all__ = ["fetch_menu", "fetch_sandwiches"]

headers = {"User-Agent": f"ugent-food (v{__version__})"}


async def fetch_menu(client_session: ClientSession, day: date, language: str) -> Menu:
    """Get the menu for a given day"""
    endpoint = f"https://hydra.ugent.be/api/2.0/resto/menu/{language}/{day.year}/{day.month}/{day.day}.json"
    async with client_session.get(endpoint, headers=headers) as response:
        if response.status == HTTPStatus.NOT_FOUND:
            raise NoMenuFound

        if response.status != HTTPStatus.OK:
            raise APIException(response.status)

        data = await response.json()
        return from_dict(Menu, data, config=Config(cast=[Enum]))


async def fetch_sandwiches(client_session: ClientSession) -> list[Sandwich]:
    """Get the list of available sandwiches"""
    endpoint = "https://hydra.ugent.be/api/2.0/resto/sandwiches.json"
    async with client_session.get(endpoint, headers=headers) as response:
        if response.status != HTTPStatus.OK:
            raise APIException(response.status)

        data = await response.json()
        return list(map(lambda x: from_dict(Sandwich, x), data))
