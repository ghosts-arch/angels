# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from dataclasses import MISSING
from typing import List, cast
import discord
import discord.types
import discord.types.snowflake

import src.core.client as client
from src.core.embeds import Embed
from src.utils.logger import Logger
from src.utils.types import Argument

logger = Logger()


class Context:

    def __init__(self, interaction: discord.Interaction):
        self.__interaction = interaction
        if not interaction.data:
            raise ValueError("Interaction data is missing")
        self.__name: str = str(interaction.data.get("name"))
        self.__options = interaction.data.get("options")
        self.__subcommand: str | None = (
            str(self.__options[0].get("name")) if self.__options else None
        )
        self.__arguments = self.__options[0].get("options") if self.__options else []
        self.__guild = interaction.guild
        self.__channel = interaction.channel
        self.__client = cast(client.Angels, self.interaction.client)
        self.__user = interaction.user

    @property
    def client(self):
        return self.__client

    @property
    def options(self):
        return self.__options

    @property
    def name(self):
        return self.__name

    @property
    def guild(self):
        return self.__guild

    @property
    def channel(self):
        return self.__channel

    @property
    def interaction(self):
        return self.__interaction

    @property
    def user(self):
        return self.__user

    @property
    def arguments(self):
        return self.__arguments

    @property
    def subcommand(self):
        return self.__subcommand

    async def send(
        self,
        content: str | None = None,
        embed: Embed | None = None,
        file=None,
        view: discord.ui.View | None = None,
    ):
        """Envoie la reponse dans le salon du message."""

        if not self.guild:
            return

        if not self.channel:
            return

        response = {}

        if content:
            response["content"] = content
        if embed:
            response["embed"] = embed
        if file:
            response["file"] = file
        if view:
            response["view"] = view

        if not (self.channel.permissions_for(self.guild.me).send_messages):
            logger.warn("Bot not have permission to send message")
            return

        try:
            response = await self.interaction.response.send_message(**response)
        except Exception as e:
            logger.error(e)
        return response

    async def send_in_channel(
        self,
        channel_id: int,
        content: str | None = None,
        embed: Embed | None = None,
        file=None,
        view: discord.ui.View | None = None,
    ):
        if not self.guild:
            raise Exception("This command is only available in a guild")
        channel = self.guild.get_channel(channel_id)
        if not channel:
            raise Exception("Channel not found")
        if not isinstance(channel, discord.TextChannel):
            raise Exception("Channel is not a text channel")
        data = {}
        if content:
            data["content"] = content
        if embed:
            data["embed"] = embed
        if file:
            data["file"] = file
        if view:
            data["view"] = view
            response = await channel.send(**data)
            await self.interaction.response.send_message(content="✅", ephemeral=True)
        return response
