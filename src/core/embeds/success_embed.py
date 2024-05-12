# coding : utf-8
# Python 3.10
# ---------------------------------------------------------------------------

import discord
from .embed import Embed


class SuccessEmbed(Embed):
    def __init__(
        self, description: str | None = None, title: str | None = None
    ) -> None:
        super().__init__(
            title=title, description=description, color=discord.Color.green()
        )
