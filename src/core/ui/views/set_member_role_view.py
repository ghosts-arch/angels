import discord

from src.core.client import Angels
from src.core.embeds import ErrorEmbed, SuccessEmbed


class SetMemberRoleView(discord.ui.View):
    def __init__(self, guild_roles):
        super().__init__()
        self.__guild_roles = guild_roles
        self.member_role_select = discord.ui.Select(
            custom_id="member_role_select",
            placeholder="Rôle de membre",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id),
                )
                for role in guild_roles
            ],
        )
        self.member_role_select.callback = self.on_select
        self.add_item(self.member_role_select)

    async def on_select(self, interaction: discord.Interaction[Angels]):
        if not interaction.data:
            raise Exception("No data")
        if not interaction.data.get("values"):
            raise Exception("No values")
        member_id = interaction.data.get("values")[0]
        successEmbed = SuccessEmbed(description=f"Rôle de membre modifié avec succès")
        await interaction.response.send_message(embed=successEmbed)
