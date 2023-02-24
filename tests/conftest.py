from enum import Enum
from typing import Type, TypeVar

import pytest
from dacite import Config, from_dict

T = TypeVar("T")


@pytest.fixture()
def create_model():
    """Fixture that returns a helper function to initialize dataclasses from dicts"""

    def _inner(cls: Type[T], data: dict) -> T:
        return from_dict(cls, data, Config(cast=[Enum]))

    return _inner
