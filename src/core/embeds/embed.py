# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import discord


class Embed(discord.Embed):

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        color: int | discord.Color | None = None,
        url: str | None = None,
    ) -> None:

        super().__init__(
            title=title,
            description=description,
            color=color if color is not None else discord.Color.dark_blue(),
            url=url,
        )

    def set_description(self, description: str):
        self.description = description
        return self

    def set_title(self, title: str):
        self.title = title
        return self
