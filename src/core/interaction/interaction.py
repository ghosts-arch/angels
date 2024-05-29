# conding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Any, Coroutine, NotRequired, TypedDict


from .context import Context


class OptionChoice(TypedDict):
    name: str
    value: str


class Option(TypedDict):
    name: str
    description: str
    type: int
    required: NotRequired[bool]
    choices: NotRequired[list[OptionChoice]]
    options: NotRequired[list]


class Interaction(ABC):
    name: str
    description: str
    options: list[Option] = []
    adminstration_channel_only: bool = False
    moderator_only: bool = False
    private_command: bool = False

    def __init__(self) -> None:
        pass

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_options(self) -> list[Option]:
        return self.options

    @abstractmethod
    def run(self, context: Context) -> Coroutine[Any, Any, Any]:
        pass

    def in_adminstration_channel_only(self) -> bool:
        return self.adminstration_channel_only

    def run_by_moderator_only(self) -> bool:
        return self.moderator_only
