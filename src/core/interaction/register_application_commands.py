# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import os
import traceback
import discord
import requests
import dotenv
import asyncio

from types import ModuleType
from typing import Dict

from .interaction import Interaction
from src.utils.logger import Logger


path = dotenv.find_dotenv()

application_id = dotenv.get_key(
    dotenv_path=path, key_to_get="APPLICATION_ID", encoding="utf-8"
)
bot_token = dotenv.get_key(
    dotenv_path=path, key_to_get="CLIENT_TOKEN", encoding="utf-8"
)

url = f"https://discord.com/api/v10/applications/{application_id}/commands"
headers = {
    "Authorization": f"Bot {bot_token}",
}


def update_command_to_discord(
    application_command_name: str, application_command: Interaction
):
    payload = {
        "name": application_command_name,
        "type": 1,
        "description": application_command.get_description(),
    }

    if hasattr(application_command, "options"):
        payload["options"] = application_command.get_options()

    try:
        response = requests.post(url, headers=headers, json=payload)
    except Exception:
        Logger.error(traceback.format_exc())

    if response.status_code != requests.codes.ok:
        Logger.error(f"/!\\ '{application_command_name}' not updated.")


async def register_application_commands(
    application_commands: Dict[str, Interaction]
) -> None:
    for data in application_commands.items():
        try:
            update_command_to_discord(*data)
            await asyncio.sleep(5)
        except Exception:
            Logger.error(traceback.format_exc())
