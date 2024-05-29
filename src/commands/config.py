import discord
import discord.types
import discord.types.snowflake


from src.core.ui.views import ConfigMenuView


from src.core.embeds import Embed
from src.core.interaction import Interaction, Context


class ApplicationCommand(Interaction):
    def __init__(self) -> None:
        self.name = "configuration"
        self.description = "Configuration du bot"
        self.moderator_only = True
        self.options = []

    async def run(self, context: Context):
        if not context.guild:
            raise Exception("This command is only available in guilds")
        if not context.client.user:
            raise Exception("Bot is not logged in.")
        embed = (
            Embed()
            .set_title(f"Configuration de {context.client.user.name}")
            .set_description(
                "1. Choix du role à donner aux membres qui valident le reglement\n2. choix du salon ou sera affiché le reglement"
            )
        )

        config_menu = ConfigMenuView()
        await context.send(embed=embed, view=config_menu)
        return
