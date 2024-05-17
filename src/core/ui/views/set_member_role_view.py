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
        if not interaction.guild:
            raise Exception("This view is only available in servers.")
        role_id = interaction.data.get("values")[0]
        interaction.client.database.set_member_role(
            guild_id=interaction.guild.id, role_id=role_id
        )
        role = interaction.guild.get_role(int(role_id))
        if not role:
            raise Exception("This role does not exists anymore.")
        successEmbed = SuccessEmbed(
            description=f"Le rôle '{role.name}' sera attribué à tous les membres qui accepteront le reglement"
        )
        await interaction.response.send_message(embed=successEmbed)
