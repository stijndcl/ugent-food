from __future__ import annotations

import json
import sys
from dataclasses import Field, dataclass, field, fields
from pathlib import Path
from typing import Optional

import click

__all__ = ["CONFIG_CHOICES"]

from dacite import from_dict

from ugent_food.cli.parsers import parse_arg_to_type
from ugent_food.i18n import Language, Translator

CONFIG_PATH = Path.home() / ".ugent_food"
CONFIG_CHOICES = ["hidden", "language", "skip_weekends"]
CONFIG_DEFAULTS = {"hidden": [], "language": "en", "skip_weekends": True}


def ensure_config_file():
    """Make an empty config file if there's none present."""
    if not CONFIG_PATH.exists():
        with CONFIG_PATH.open("w+", encoding="utf-8") as fp:
            json.dump({}, fp)

        click.echo(f"Created configuration file {CONFIG_PATH}.")


def load_config_file() -> dict:
    """Load the config file"""
    ensure_config_file()
    with CONFIG_PATH.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@dataclass
class Config:
    """Class to load & store settings to configure the tool"""

    language: str = field(  # type: ignore # Mypy doesn't enjoy this one
        default=CONFIG_DEFAULTS["language"],
        metadata={
            "description": "The language used to fetch the menus in. "
            'Supported values are "en" (English) and "nl" (Dutch).'
            "\nNote that not every endpoint is available in every language.",
            "allowed": ["en", "nl"],
        },
    )
    skip_weekends: bool = field(  # type: ignore # Mypy doesn't enjoy this one
        default=CONFIG_DEFAULTS["skip_weekends"],
        metadata={
            "description": "Whether to automatically skip weekends when fetching menus. "
            "This defaults to True because the restaurants aren't usually open during weekends."
            "\nUsing the tool on a Saturday (with this setting set to True) will show "
            "the menu for the coming Monday instead."
        },
    )
    _language: Optional[Language] = field(init=False, default=None)
    translator: Translator = field(init=False)

    def __post_init__(self):
        """Initialize fields that depend on the config settings"""
        self.language = self.language.lower()

        # Find the Language instance that matches the setting
        for language in Language:
            if language.value == self.language:
                self._language = language
                break

        # Nothing found
        if self._language is None:
            raise ValueError(f"Invalid language configuration: {self.language}")

        self.translator = Translator(language=self._language)

    @classmethod
    def _find_field(cls, name: str) -> Optional[Field]:
        """Try to find a field by its name"""
        # Allow dashes instead of underscores
        name = name.replace("-", "_").lower()

        matched_field: Optional[Field] = None

        for _field in fields(cls):
            # Ignore fields that aren't meant to be configured
            if not _field.init:
                continue

            if _field.name == name:
                matched_field = _field
                break

        return matched_field

    @classmethod
    def load(cls) -> Config:
        """Create a Config instance by loading the configuration file"""
        content = load_config_file()

        return from_dict(cls, content)

    @classmethod
    def set(cls, name: str, value: str):
        """Change a setting"""
        matched_field = Config._find_field(name)

        # Found no field
        if matched_field is None:
            click.echo(f"Unknown setting: {name}.")
            sys.exit(1)

        try:
            converted_value = parse_arg_to_type(value, matched_field.type)
        except ValueError:
            click.echo(f'Unable to parse "{value}" to type {matched_field.type}.')
            sys.exit(1)

        # Value is not allowed for this field
        allowed_values = matched_field.metadata.get("allowed", [])
        if value not in allowed_values:
            click.echo(
                f'Illegal value "{value}" for setting "{matched_field.name}".\n'
                f"Accepted values are: {', '.join(allowed_values)}"
            )
            sys.exit(1)

        config = load_config_file()
        config[matched_field.name] = converted_value

        with CONFIG_PATH.open("w", encoding="utf-8") as fp:
            json.dump(config, fp)
