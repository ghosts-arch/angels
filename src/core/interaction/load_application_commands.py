# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import os
import importlib

from types import ModuleType
from typing import Dict

from .interaction import Interaction


def load_application_commands() -> Dict[str, Interaction]:

    application_commands: Dict[str, Interaction] = {}
    files = filter(lambda f: f.endswith(".py"), os.listdir("src/commands"))

    for f in files:
        module_name = os.path.splitext(f)[0]
        module = importlib.import_module(name=f".{module_name}", package="src.commands")

        if not is_application_command(module):
            raise Exception(f"/!\\ '{module}' n'est pas une commande valide")

        application_command: Interaction = module.ApplicationCommand()
        application_commands[application_command.get_name()] = application_command

    return application_commands


def is_application_command(module: ModuleType) -> bool:
    return hasattr(module, "ApplicationCommand") and issubclass(
        module.ApplicationCommand, Interaction
    )
