import discord
from src.core.client import Angels
from src.core.ui.buttons import CancelationButton, ConfirmationButton


class AcceptRulesView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.decline_rules_button = CancelationButton(
            label="Refuser", custom_id="decline_rules", callback=self.decline_rules
        )
        self.add_item(self.decline_rules_button)
        self.accept_rules_button = ConfirmationButton(
            label="Accepter", custom_id="accept_rules", callback=self.accept_rules
        )
        self.add_item(self.accept_rules_button)

    def decline_rules(self, interaction: discord.Interaction):
        pass

    async def accept_rules(self, interaction: discord.Interaction[Angels]):
        print("0")
        if not interaction.guild:
            raise Exception("This button is only available in servers.")
        guild = interaction.client.database.find_guild(guild_id=interaction.guild.id)
        validated_reglement_role_id = guild.get_member_role_id()
        if not validated_reglement_role_id:
            raise Exception("Pas de role defini pour cette guilde")
        role = interaction.guild.get_role(validated_reglement_role_id)
        print(role)
        if not role:
            raise Exception("This role does not exists anymore")
        if not isinstance(interaction.user, discord.Member):
            raise Exception()

        await interaction.user.add_roles(role)
