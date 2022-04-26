from __future__ import annotations

import json
import sys
from dataclasses import field, fields, dataclass
from pathlib import Path
from typing import Optional

from dacite import from_dict
from tabulate import tabulate

from ugent_food.cli.converters import cast_to_type
from ugent_food.data.enums import Language
from ugent_food.i18n import Translator

__all__ = [
    "Config",
    "mode_config"
]

# Path to the configuration file
config_path = Path(f"{Path.home()}/.ugent_food")


def ensure_config_file():
    """Make an empty config file if there's none present."""
    if not config_path.exists():
        with config_path.open("w+", encoding="utf-8") as fp:
            json.dump({}, fp)


def load_config_file() -> dict:
    """Load an existing config file"""
    with config_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


@dataclass
class Config:
    """Class to load & store settings on the user's system
    Allows configuration of the tool.
    """
    language: str = field(default="en", metadata={
        "description": "The language used to fetch the menus in. "
                       "Supported values are currently \"en\" (English) and \"nl\" (Dutch).",
        "allowed": ["en", "nl"]
    })
    skip_weekends: bool = field(default=True, metadata={
        "description": "Whether to automatically skip weekends when fetching menus. "
                       "This defaults to true because the restaurants aren't usually open during weekends. "
                       "For example: using the tool on a Saturday will show the menu for the coming Monday.",
        "allowed": [True, False]
    })
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
        ensure_config_file()
        content = load_config_file()

        return from_dict(cls, content)

    @classmethod
    def set(cls, name: str, value: str):
        """Change a configuration"""
        # Allow dashes instead of underscores to be used
        value.replace("-", "_")

        matched_field = None

        for _field in sorted(fields(cls), key=lambda x: x.name):
            if not _field.init:
                continue

            if _field.name == name:
                matched_field = _field
                break

        # No field found with this name
        if matched_field is None:
            print(f"Unknown setting: {name}.", file=sys.stderr)
            sys.exit(1)

        cast_value = cast_to_type(str(matched_field.type), value)

        if cast_value is None:
            allowed_values = matched_field.metadata.get("allowed", [])

            if value not in allowed_values:
                allowed_values_str = list(map(str, allowed_values))
                print(f"Illegal value for setting \"{name}\": \"{value}\".\n"
                      f"Accepted values are: {', '.join(allowed_values_str)}.", file=sys.stderr
                      )
                sys.exit(2)

        # Change the setting & dump it back into the file
        with config_path.open("r", encoding="utf-8") as fp:
            content = json.load(fp)

        with config_path.open("w", encoding="utf-8") as fp:
            content[name] = cast_value
            json.dump(content, fp)

    def ls(self, table_type: str = "simple"):
        """Print all configuration options (including descriptions)"""
        field_data = []

        for _field in sorted(fields(self), key=lambda x: x.name):
            if not _field.init:
                continue

            field_data.append([
                _field.name,
                _field.type,
                _field.metadata["description"],
                _field.default,
                self.__getattribute__(_field.name)
            ])

        print(tabulate(field_data, headers=[
            "Name", "Type", "Description", "Default value", "Value"
        ], tablefmt=table_type))


def mode_config(config: Config, args: dict):
    """Main method to handle configuration
    Parses arguments and chooses the correct subcommand
    """
    if args.get("subcommand") == "ls":
        # Error if any extra arguments were passed
        illegal_args = ["target", "value"]
        illegal_args_passed = list(key for key in args.keys() if key in illegal_args and args[key] is not None)

        if illegal_args_passed:
            print(f"Unexpected arguments: {', '.join(illegal_args_passed)}", file=sys.stderr)
            sys.exit(3)

        config.ls()
    elif args.get("subcommand") == "set":
        required_args = ["target", "value"]

        # Check if all required args are present
        for arg in required_args:
            if args.get(arg, None) is None:
                print(f"Missing argument: {arg}.", file=sys.stderr)
                sys.exit(4)

        Config.set(args["target"], args["value"])
