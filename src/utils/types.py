from typing import Any, TypedDict, NotRequired
from enum import Enum
import discord


class Permissions(Enum):
    IN_DEV_CHANNEL = 1
    IS_ADMIN = 2


class OptionChoice(TypedDict):
    name: str
    value: str


class Option(TypedDict):
    name: str
    description: str
    type: int
    required: NotRequired[bool]
    choices: NotRequired[list[OptionChoice]]


class Argument(TypedDict):
    name: str
    value: Any
    type: int
