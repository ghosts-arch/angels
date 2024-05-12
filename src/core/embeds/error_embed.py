# coding : utf-8
# Python 3.10
# ---------------------------------------------------------------------------

import discord

from .embed import Embed


class ErrorEmbed(Embed):
    def __init__(
        self,
        description: str | None = None,
    ) -> None:
        super().__init__(description=description, color=discord.Color.red())
