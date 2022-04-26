from __future__ import annotations

from enum import Enum, auto


class Kind(Enum):
    """Enum for a kind of dish"""
    FISH = "fish"
    MEAT = "meat"
    SOUP = "soup"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"

    @classmethod
    def from_str(cls, value: str) -> Kind:
        """Get an Enum value from the string value"""
        for key in cls:
            if key.value == value.lower():
                return key

        raise ValueError(f"Unknown kind: \"{value}\".")


class Type(Enum):
    """Enum for a type of dish"""
    COLD = "cold"
    MAIN = "main"
    SIDE = "side"

    @classmethod
    def from_str(cls, value: str) -> Type:
        """Get an Enum value from the string value"""
        for key in cls:
            if key.value == value.lower():
                return key

        raise ValueError(f"Unsupported type: \"{value}\".")


class Language(Enum):
    """Enum for all the different supported languages"""
    NL = "nl"
    EN = "en"

    @classmethod
    def from_str(cls, language: str) -> Language:
        """Get an Enum value from the string value"""
        for key in cls:
            if key.value == language.lower():
                return key

        raise ValueError(f"Unsupported language: \"{language}\".")


class Message(Enum):
    """Enum for the messages that can be displayed in every language"""
    RESTO_CLOSED = auto()
    MENU_FOR = auto()

    # Types of meals
    SOUP = auto()
    MAIN_COURSE = auto()
    VEGETABLES = auto()
