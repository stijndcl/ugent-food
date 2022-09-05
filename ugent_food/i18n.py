from __future__ import annotations

from enum import Enum, auto

from ugent_food.api.enums import MealKind, MealType

__all__ = ["Language", "Message", "Translator"]


class Language(Enum):
    """Enum for supported languages to choose from"""

    DUTCH = "nl"
    ENGLISH = "en"

    @classmethod
    def from_str(cls, language: str) -> Language:
        """Get an Enum value from the string value"""
        for key in cls:
            if key.value == language.lower():
                return key

        raise ValueError(f'Unsupported language: "{language}".')


class Message(Enum):
    """Enum for messages that can be displayed in multiple languages"""

    MENU_FOR = auto()
    RESTO_CLOSED = auto()

    MAIN_COURSE = auto()
    SOUP = auto()
    VEGETABLES = auto()


kinds: dict[MealKind, dict[Language, str]] = {
    MealKind.FISH: {Language.ENGLISH: "Fish", Language.DUTCH: "Vis"},
    MealKind.MEAT: {Language.ENGLISH: "Meat", Language.DUTCH: "Vlees"},
    MealKind.SOUP: {Language.ENGLISH: "Soup", Language.DUTCH: "Soep"},
    MealKind.VEGAN: {Language.ENGLISH: "Vegan", Language.DUTCH: "Vegan"},
    MealKind.VEGETARIAN: {Language.ENGLISH: "Vegetarian", Language.DUTCH: "Vegetarisch"},
}


types: dict[MealType, dict[Language, str]] = {
    MealType.MAIN: {Language.ENGLISH: "Main course", Language.DUTCH: "Hoofdgerecht"},
    MealType.COLD: {Language.ENGLISH: "Cold", Language.DUTCH: "Koud"},
    MealType.SIDE: {Language.ENGLISH: "Side dish", Language.DUTCH: "Bijgerecht"},
}


messages: dict[Message, dict[Language, str]] = {
    Message.RESTO_CLOSED: {
        Language.ENGLISH: "The restaurants are closed on {day}.",
        Language.DUTCH: "De resto's zijn gesloten op {day}.",
    },
    Message.MENU_FOR: {Language.ENGLISH: "Menu for {weekday} {day}:", Language.DUTCH: "Menu voor {weekday} {day}:"},
    Message.VEGETABLES: {Language.ENGLISH: "Vegetables:\n{vegetables}", Language.DUTCH: "Groenten:\n{vegetables}"},
}


weekdays: dict[int, dict[Language, str]] = {
    0: {Language.ENGLISH: "Monday", Language.DUTCH: "maandag"},
    1: {Language.ENGLISH: "Tuesday", Language.DUTCH: "dinsdag"},
    2: {Language.ENGLISH: "Wednesday", Language.DUTCH: "woensdag"},
    3: {Language.ENGLISH: "Thursday", Language.DUTCH: "donderdag"},
    4: {Language.ENGLISH: "Friday", Language.DUTCH: "vrijdag"},
    5: {Language.ENGLISH: "Saturday", Language.DUTCH: "zaterdag"},
    6: {Language.ENGLISH: "Sunday", Language.DUTCH: "zondag"},
}


class Translator:
    """Class that handles translation of messages"""

    language: Language

    def __init__(self, language: Language):
        self.language = language

    def kind(self, kind: MealKind) -> str:
        """Get a translation for a meal kind in the configured language"""
        return kinds[kind][self.language]

    def type(self, type_: MealType) -> str:
        """Get a translation for a type in the configured language"""
        return types[type_][self.language]

    def message(self, message: Message, **kwargs) -> str:
        """Get a specific message in the configured language"""
        return messages[message][self.language].format(**kwargs)

    def weekday(self, weekday: int) -> str:
        """Get a day of the week in a configured language"""
        return weekdays[weekday][self.language]
