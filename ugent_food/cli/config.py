import json
from pathlib import Path

import click

__all__ = ["CONFIG_CHOICES"]

CONFIG_PATH = Path.home() / ".ugent_food"
CONFIG_CHOICES = ["hidden", "language", "skip_weekends"]
CONFIG_DEFAULTS = {"hidden": [], "language": "en", "skip_weekends": True}


def ensure_config_file():
    """Make an empty config file if there's none present."""
    if not CONFIG_PATH.exists():
        with CONFIG_PATH.open("w+", encoding="utf-8") as fp:
            json.dump({}, fp)

        click.echo(f"Created configuration file {CONFIG_PATH}.")
