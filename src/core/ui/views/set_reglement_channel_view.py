from typing import Sequence
import discord
from src.core.embeds import Embed
import src.core.client as client
from src.core.embeds import ErrorEmbed, SuccessEmbed
from src.core.ui.buttons import ConfigMenuButton, CancelationButton


class SetReglementChannelView(discord.ui.View):
    def __init__(
        self,
        guild_channels: Sequence[discord.guild.abc.GuildChannel],
        timeout: int = 240,
    ):
        super().__init__(timeout=timeout)

        self.reglement_channel_select = discord.ui.Select(
            custom_id="member_role_select",
            placeholder="canal du reglement",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=channel.name,
                    value=str(channel.id),
                )
                for channel in sorted(guild_channels, key=lambda x: x.position)
                if channel.type == discord.ChannelType.text
            ],
        )
        self.reglement_channel_select.callback = self.on_select
        self.add_item(self.reglement_channel_select)
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
        channel_id = interaction.data.get("values")[0]
        interaction.client.database.set_reglement_channel_id(
            guild_id=interaction.guild.id, channel_id=channel_id
        )
        channel = interaction.guild.get_channel(int(channel_id))
        if not channel:
            raise Exception("This channel doesn't exist.")
        successEmbed = SuccessEmbed(
            description=f"Le reglement sera envoyé dans le canal {channel.name}."
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
