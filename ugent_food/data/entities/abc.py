import abc
from dataclasses import dataclass
from datetime import datetime

from ugent_food.modes.config import Config


@dataclass
class MenuMixin:
    """Mixin class to make Mypy happy"""


class Menu(abc.ABC, MenuMixin):
    """Abstract class for menu's"""

    @abc.abstractmethod
    def print_menu(self, config: Config, date: datetime):
        """Abstract method that all Menu's should implement
        Print the menu to the terminal
        """
        raise NotImplementedError
