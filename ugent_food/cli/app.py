import sys
from typing import Optional

import click
from aiohttp import ClientSession

from ugent_food.api.wrapper import fetch_menu, fetch_sandwiches
from ugent_food.exceptions import APIException, NoMenuFound
from ugent_food.version import __version__

from .async_command import async_command
from .config import CONFIG_CHOICES, Config
from .default_group import DefaultGroup
from .parsers import parse_date_argument
from .tables import sandwich_table

__all__ = ["cli"]


# Load config by default because every command needs it
user_config = Config.load()


@click.group(cls=DefaultGroup, default="menu", invoke_without_command=True)
@click.option(
    "-V", "--version", is_flag=True, show_default=False, default=False, help="Show the version number and exit."
)
@click.pass_context
@async_command
async def cli(ctx: click.Context, version: bool = False):
    """Command-line tool to get the current menu for Ghent University restaurants

    Running this command without any subcommands is an alias to "menu".
    """
    # If a subcommand was invoked as well, do nothing here
    # let that subcommand handle it
    if ctx.invoked_subcommand is not None:
        return

    # Print version number & exit
    if version:
        click.echo(f"ugent-food v{__version__}")
        ctx.exit(0)


@cli.group(cls=DefaultGroup, default="ls", invoke_without_command=True)
@click.pass_context
def config(ctx: click.Context):
    """Read or modify settings.

    Running this command without any subcommands is an alias to "config ls".
    """


@config.command(name="ls")
def config_ls():
    """Display a list of settings, along with their current and accepted values."""
    user_config.ls()


@config.command(name="reset")
@click.argument("name", type=click.Choice(CONFIG_CHOICES))
def config_reset(name: str):
    """Reset setting NAME back to its default value."""
    Config.reset(name)


@config.command(name="set")
@click.argument("name", type=click.Choice(CONFIG_CHOICES))
@click.argument("value")
def config_set(name: str, value: str):
    """Change the value of setting NAME to VALUE."""
    Config.set(name, value)


@cli.command(name="menu")
@click.argument("day", required=False)
@async_command
async def menu_fetcher(day: Optional[str] = None):
    """Fetch the menu for DAY.

    The DAY-argument supports DD/MM(/YYYY) formats, as well as Dutch and English weekdays and relative offsets.
    If no value is provided, the menu for today is fetched instead.
    """
    # Try to parse the date arg
    date_instance = parse_date_argument(day)

    # Parsing failed
    if date_instance is None:
        click.echo(f'Unable to parse argument "{day}".')
        sys.exit(1)

    async with ClientSession() as session:
        try:
            menu = await fetch_menu(session, date_instance, "nl")
            click.echo(menu.to_string(user_config, date_instance))
        except APIException as e:
            click.echo(e)
            sys.exit(1)
        except NoMenuFound:
            click.echo(f"No menu found for {date_instance} (parsed from {day}).")
            sys.exit(1)


@cli.command()
@async_command
async def sandwiches():
    """Show the list of sandwiches available in restaurants.

    Note: this endpoint is only available in Dutch.
    """
    async with ClientSession() as session:
        try:
            sandwich_list = await fetch_sandwiches(session)
            click.echo(sandwich_table(sandwich_list, user_config.translator))
        except APIException as e:
            click.echo(e)
            sys.exit(1)
