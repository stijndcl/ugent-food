from __future__ import annotations

import json
import sys
import textwrap
from dataclasses import MISSING, Field, dataclass, field, fields
from pathlib import Path
from typing import Any, Optional

import click
from dacite import from_dict
from tabulate import tabulate

from ugent_food.cli.parsers import parse_arg_to_type
from ugent_food.i18n import Language, Translator

__all__ = ["CONFIG_CHOICES", "Config"]

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

    hidden: list[str] = field(  # type: ignore # Mypy doesn't enjoy this one
        default_factory=list,
        metadata={
            "description": "A list of meal kinds that should be hidden when fetching menus."
            "\nThis can be useful for vegetarians and vegans who don't care about the meat dishes.",
            "comparable_type": list,
        },
    )

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
        # Find the Language instance that matches the setting
        self._language = Language.from_str(self.language)
        self.translator = Translator(language=self._language)

        # Make sure "hidden" values are lowercase
        self.hidden = list(map(str.lower, self.hidden))

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
    def _get_field_default(cls, field_: Field) -> Any:
        """Get the default value for a field"""
        if field_.default != MISSING:
            return field_.default

        # If there is no default value, check if there's a factory instead
        if field_.default_factory != MISSING and callable(field_.default_factory):
            return field_.default_factory()

        return MISSING

    def ls(self):
        """Print the user's configuration settings."""
        table_data = []
        for _field in fields(self):
            if not _field.init:
                continue

            description = "\n".join(textwrap.wrap(_field.metadata.get("description")))
            default = self._get_field_default(_field)

            table_data.append(
                [
                    _field.name,
                    description,
                    default if default != MISSING else "",
                    getattr(self, _field.name),
                ]
            )

        click.echo(tabulate(table_data, headers=["name", "description", "default", "value"]))

    @classmethod
    def load(cls) -> Config:
        """Create a Config instance by loading the configuration file"""
        content = load_config_file()

        return from_dict(cls, content)

    @classmethod
    def reset(cls, name: str):
        """Reset a setting back to its default value"""
        matched_field = Config._find_field(name)

        # Found no field
        if matched_field is None:
            click.echo(f"Unknown setting: {name}.")
            sys.exit(1)

        config = load_config_file()
        config[matched_field.name] = CONFIG_DEFAULTS[matched_field.name]

        with CONFIG_PATH.open("w", encoding="utf-8") as fp:
            json.dump(config, fp)

        click.echo(f'Restored setting "{matched_field.name}" back to "{CONFIG_DEFAULTS[matched_field.name]}".')

    @classmethod
    def set(cls, name: str, value: str):
        """Change a setting"""
        matched_field = Config._find_field(name)

        # Found no field
        if matched_field is None:
            click.echo(f"Unknown setting: {name}.")
            sys.exit(1)

        field_type = matched_field.metadata.get("comparable_type", matched_field.type)

        try:
            converted_value = parse_arg_to_type(value, field_type)
        except ValueError:
            click.echo(f'Unable to parse "{value}" to type {field_type}.')
            sys.exit(1)

        # Value is not allowed for this field
        allowed_values = matched_field.metadata.get("allowed", [])
        if allowed_values and value not in allowed_values:
            click.echo(
                f'Illegal value "{value}" for setting "{matched_field.name}".\n'
                f"Accepted values are: {', '.join(allowed_values)}"
            )
            sys.exit(1)

        config = load_config_file()
        config[matched_field.name] = converted_value

        with CONFIG_PATH.open("w", encoding="utf-8") as fp:
            json.dump(config, fp)
