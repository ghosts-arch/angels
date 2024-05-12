import discord


class CancelationButton(discord.ui.Button):
    def __init__(self, label: str, custom_id: str, callback):
        super().__init__(
            label=label, style=discord.ButtonStyle.red, custom_id=custom_id
        )
        self.callback = callback
