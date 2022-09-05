from typing import Optional

import click
from click import Context

__all__ = ["DefaultGroup"]


class DefaultGroup(click.Group):
    """Click Group command that invokes a default command if no subcommands matched

    This is a trimmed down version of click-default-group without features I don't care about
    (and proper type hinting)
    """

    default: Optional[str]

    def __init__(self, *args, **kwargs):
        self.ignore_unknown_options = True
        self.default = kwargs.pop("default", None)
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
        """Modify the parser to insert the default command name if no arguments were passed"""
        if not args and self.default is not None:
            args.insert(0, self.default)

        return super().parse_args(ctx, args)

    def get_command(self, ctx: Context, cmd_name: str):
        """If no subcommands matched, store the name argument and pass the default command onwards

        By storing the first argument we don't "lose" it when we still need it later on
        to pass it into the subcommand
        """
        if self.default is not None and cmd_name not in self.commands:
            # No command name matched.
            setattr(ctx, "arg0", cmd_name)  # noqa: B010
            cmd_name = self.default
        return super().get_command(ctx, cmd_name)

    def resolve_command(self, ctx: Context, args: list[str]):
        """If a subcommand was found, restore the original arguments if necessary

        get_command() modified the list of args, so pull the original argument back out
        """
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        if hasattr(ctx, "arg0") and cmd is not None:
            args.insert(0, getattr(ctx, "arg0"))  # noqa: B009
            cmd_name = cmd.name
        return cmd_name, cmd, args
