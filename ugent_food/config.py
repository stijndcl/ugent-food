from __future__ import annotations

import json
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional

from dacite import from_dict

from ugent_food.data.enums import Language
from ugent_food.i18n import Translator


@dataclass
class Config:
    language: str = "en"
    _language: Optional[Language] = field(init=False, default=None)
    translator: Translator = field(init=False)

    def __post_init__(self):
        """Initialize fields that depend on the config settings"""
        self.language = self.language.lower()

        # Try to find the correct language first
        for language in Language:
            if language.value == self.language:
                self._language = language
                break

        if self._language is None:
            raise ValueError(f"Invalid language configuration: {self.language}")

        # Create translator
        self.translator = Translator(language=self._language)

    @classmethod
    def load(cls) -> Config:
        """Load configuration from the file"""
        # Create file if it doesn't exist
        config_path = Path(f"{Path.home()}/.ugent_food")
        if not config_path.exists():
            with config_path.open("w+", encoding="utf-8") as fp:
                json.dump({}, fp)

        with open(config_path, "r+") as fp:
            content = json.load(fp)

        return from_dict(cls, content)

