from typing import Any, Callable, Optional


def to_bool(argument: str) -> Optional[bool]:
    """Turn a string argument into a bool"""
    if argument.lower() in ["true", "t", "1"]:
        return True

    if argument.lower() in ["false", "f", "0"]:
        return False

    return None


def cast_to_type(type_: str, value: str) -> Optional[Any]:
    """Cast an argument to the required type"""
    type_dict: dict[str, Callable[[str], Optional[Any]]] = {
        "bool": to_bool,
        "str": lambda x: x
    }

    return type_dict[type_](value)
