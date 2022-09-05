import asyncio
import functools
from typing import Any, Callable

__all__ = ["async_command"]


def async_command(func: Callable[..., Any]):
    """Decorator to make Click support async commands

    Based on https://github.com/pallets/click/issues/85#issuecomment-503464628
    """

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        # Run in active event loop if one exists, otherwise create a new one

        try:
            loop = asyncio.get_running_loop()

            if loop and loop.is_running():
                return loop.create_task(func(*args, **kwargs))
        except RuntimeError:
            pass

        return asyncio.run(func(*args, **kwargs))

    return _wrapper
