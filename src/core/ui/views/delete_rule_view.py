import discord

import src.core.client as client
from src.core.embeds import SuccessEmbed, ErrorEmbed
from src.core.ui.buttons import CancelationButton, ConfirmationButton


class DeleteRuleView(discord.ui.View):
    def __init__(self, rule):
        super().__init__()
        cancel_button = CancelationButton(
            label="Annuler", custom_id="cancel_delete_rule", callback=self.on_cancel
        )
        self.add_item(cancel_button)
        confirmation_button = ConfirmationButton(
            label="Supprimer",
            custom_id=f"confirm_delete_rule_{rule.id}",
            callback=self.on_confirm,
        )
        self.add_item(confirmation_button)

    async def on_cancel(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()
        await interaction.channel.send(
            embed=ErrorEmbed(description=f"Annulation de la commande ❌")
        )

    async def on_confirm(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()
        if not interaction.data:
            raise Exception("No data")
        if not interaction.data.get("custom_id"):
            raise Exception("No custom id")
        custom_id = interaction.data.get("custom_id")
        if type(custom_id) != str:
            raise Exception("custom id must be a string")
        rule_id = custom_id.split("_")[-1]
        rule = interaction.client.database.delete_rule(rule_id=int(rule_id))
        await interaction.channel.send(
            embed=SuccessEmbed(description=f"Règle supprimée").add_field(
                name=rule.title, value=rule.content
            )
        )
