import discord
from src.core.embeds import Embed
import src.core.client as client
from src.core.embeds import ErrorEmbed, SuccessEmbed
from src.core.ui.buttons import ConfigMenuButton, CancelationButton


class SetMemberRoleView(discord.ui.View):
    def __init__(self, guild_roles, timeout: int = 240):
        super().__init__(timeout=timeout)

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
        set_config_menu_button = ConfigMenuButton(
            label="Retour au menu",
            custom_id="config_menu_button",
            callback=self.show_config_menu,
        )
        set_cancelation_button = CancelationButton(
            label="Fermer",
            custom_id="cancel_button",
            callback=self.on_cancel,
        )
        self.add_item(set_config_menu_button)
        self.add_item(set_cancelation_button)

    async def on_select(self, interaction: discord.Interaction):
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
        # original_message = await interaction.original_response()
        # await interaction.response.edit_message(view=None, embed=successEmbed)
        await interaction.channel.send(embed=successEmbed)
        await self.show_config_menu(interaction=interaction)

    async def show_config_menu(self, interaction: discord.Interaction):
        from .config_menu_view import ConfigMenuView

        embed = Embed(
            title=f"Configuration de {interaction.client.user.name}",
            description="1. Choix du role à donner aux membres qui valident le reglement\n2. choix du salon ou sera affiché le reglement",
        )

        config_menu = ConfigMenuView()
        await interaction.response.edit_message(embed=embed, view=config_menu)

    async def on_cancel(self, interaction: discord.Interaction):
        self.stop()
        await interaction.response.edit_message(
            view=None, embed=SuccessEmbed(description="Fermeture du menu")
        )
