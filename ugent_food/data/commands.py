from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Callable, Any

from ugent_food.modes import mode_menu
from ugent_food.modes.config import Config


@dataclass
class CommandData:
    argv: list[str] = field(default_factory=list)
    date: Optional[datetime] = datetime.now()


@dataclass
class Command:
    callable: Callable[[Config, CommandData], Any] = mode_menu
    data: CommandData = CommandData()

    def __call__(self, config: Config, *args, **kwargs):
        self.callable(config, self.data)
