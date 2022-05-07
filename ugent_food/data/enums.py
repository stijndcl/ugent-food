from __future__ import annotations

from enum import Enum, auto


class Kind(Enum):
    FISH = "fish"
    MEAT = "meat"
    SOUP = "soup"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"


class Type(Enum):
    COLD = "cold"
    MAIN = "main"
    SIDE = "side"


class Language(Enum):
    """Enum for all the different supported languages"""
    NL = "nl"
    EN = "en"

    @classmethod
    def from_str(cls, language: str) -> Language:
        language = language.lower()

        for key in cls:
            if key.value == language:
                return key

        raise ValueError(f"Unsupported language: \"language\".")


class Message(Enum):
    """Enum for the messages that can be displayed in every language"""
    RESTO_CLOSED = auto()
    MENU_FOR = auto()

    # Types of meals
    SOUP = auto()
    MAIN_COURSE = auto()
    VEGETABLES = auto()
