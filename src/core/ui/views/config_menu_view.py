import discord
from src.core.embeds import SuccessEmbed
from src.core.ui.buttons import SetChannelButton, SetRoleButton, CancelationButton
from .set_member_role_view import SetMemberRoleView
from .set_reglement_channel_view import SetReglementChannelView


class ConfigMenuView(discord.ui.View):
    def __init__(self, timeout: int = 240):
        super().__init__(timeout=timeout)

        self.set_role_button = SetRoleButton(
            label="Définir le rôle",
            custom_id="set_role_button",
            callback=self.show_role_select_menu,
        )
        self.add_item(self.set_role_button)
        self.set_channel_button = SetChannelButton(
            label="Définir le canal",
            custom_id="set_channel_button",
            callback=self.show_channel_select_menu,
        )
        self.add_item(self.set_channel_button)
        self.cancel_button = CancelationButton(
            label="Annuler", custom_id="cancel_button", callback=self.on_cancel
        )
        self.add_item(self.cancel_button)

    async def show_role_select_menu(self, interaction: discord.Interaction):
        set_role_view = SetMemberRoleView(guild_roles=interaction.guild.roles)
        embed = discord.Embed(
            title="Rôle de membre",
            description="Sélectionnez à attribuer aux membres qui acceptent le reglement",
        )
        await interaction.response.edit_message(embed=embed, view=set_role_view)

    async def show_channel_select_menu(self, interaction: discord.Interaction):
        set_reglement_channel_view = SetReglementChannelView(
            guild_channels=interaction.guild.channels
        )
        embed = discord.Embed(
            title="Channel du reglement",
            description="Sélectionnez le canal ou le reglement sera affiché.",
        )
        await interaction.response.edit_message(
            embed=embed, view=set_reglement_channel_view
        )

    async def on_cancel(self, interaction):
        await interaction.response.edit_message(
            view=None, embed=SuccessEmbed(description="Fermeture du menu")
        )
