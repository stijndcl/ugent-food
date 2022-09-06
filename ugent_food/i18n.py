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

    EXTRA_MESSAGE = auto()
    MENU_FOR = auto()
    RESTO_CLOSED = auto()

    MAIN_COURSE = auto()
    SOUP = auto()
    VEGETABLES = auto()


kinds: dict[MealKind, dict[Language, str]] = {
    MealKind.FISH: {Language.DUTCH: "Vis", Language.ENGLISH: "Fish"},
    MealKind.MEAT: {Language.DUTCH: "Vlees", Language.ENGLISH: "Meat"},
    MealKind.SOUP: {Language.DUTCH: "Soep", Language.ENGLISH: "Soup"},
    MealKind.VEGAN: {Language.DUTCH: "Vegan", Language.ENGLISH: "Vegan"},
    MealKind.VEGETARIAN: {Language.DUTCH: "Vegetarisch", Language.ENGLISH: "Vegetarian"},
}


types: dict[MealType, dict[Language, str]] = {
    MealType.MAIN: {Language.DUTCH: "Hoofdgerecht", Language.ENGLISH: "Main course"},
    MealType.COLD: {Language.DUTCH: "Koud", Language.ENGLISH: "Cold"},
    MealType.SIDE: {Language.DUTCH: "Bijgerecht", Language.ENGLISH: "Side dish"},
}


messages: dict[Message, dict[Language, str]] = {
    Message.EXTRA_MESSAGE: {
        Language.DUTCH: "Extra mededeling:\n{extra}",
        Language.ENGLISH: "Extra message:\n{extra}",
    },
    Message.RESTO_CLOSED: {
        Language.DUTCH: "De resto's zijn gesloten op {day}.",
        Language.ENGLISH: "The restaurants are closed on {day}.",
    },
    Message.MENU_FOR: {Language.DUTCH: "Menu voor {weekday} {day}:", Language.ENGLISH: "Menu for {weekday} {day}:"},
    Message.VEGETABLES: {Language.DUTCH: "Groenten:\n{vegetables}", Language.ENGLISH: "Vegetables:\n{vegetables}"},
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

    def menu_table_headers(self) -> list[str]:
        """Get a translation for the headers in the menu table"""
        if self.language == Language.DUTCH:
            return ["Type", "Soort", "Naam", "Prijs"]

        return ["Type", "Kind", "Name", "Price"]

    def sandwich_table_headers(self) -> list[str]:
        """Get a translation for the headers in the sandwich table"""
        if self.language == Language.DUTCH:
            return ["Naam", "Ingrediënten", "Prijs (klein)", "Prijs (medium)"]

        return ["Name", "Ingredients", "Price (small)", "Price (medium)"]

    def type(self, type_: MealType) -> str:
        """Get a translation for a type in the configured language"""
        return types[type_][self.language]

    def message(self, message: Message, **kwargs) -> str:
        """Get a specific message in the configured language"""
        return messages[message][self.language].format(**kwargs)

    def weekday(self, weekday: int) -> str:
        """Get a day of the week in a configured language"""
        return weekdays[weekday][self.language]
