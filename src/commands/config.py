import discord
import discord.types
import discord.types.snowflake


from src.core.ui.views import DeleteRuleView, SetMemberRoleView

from src.core.ui.buttons import ConfirmationButton, CancelationButton
from src.core.ui.forms import AddRuleForm, EditRuleForm
from src.core.embeds import ErrorEmbed, SuccessEmbed, Embed
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
        embed = Embed(
            title=f"Configuration de {context.client.user.name}",
            description="Choix du role à donner aux membres qui valident le reglement",
        )

        member_role_select = SetMemberRoleView(guild_roles=context.guild.roles)
        await context.send(embed=embed, view=member_role_select)
        return
