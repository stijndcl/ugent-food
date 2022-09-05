from enum import Enum

__all__ = ["Language", "Translator"]


class Language(Enum):
    """Enum for supported languages to choose from"""

    DUTCH = "nl"
    ENGLISH = "en"


class Translator:
    """Class to translate strings into the language selected by the user"""

    language: Language

    def __init__(self, language: Language):
        self.language = language
