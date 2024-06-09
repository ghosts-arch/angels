import discord
from src.core.embeds.embed import Embed
import src.core.client as client
from src.core.ui.buttons import CancelationButton, PublishRuleButton


class PublishRuleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        publish_rule_button = PublishRuleButton(
            label="Publier la règle",
            custom_id="publish_rule",
            callback=self.publish_rule,
        )
        self.add_item(publish_rule_button)
        cancelation_button = CancelationButton(
            label="Annuler", custom_id="cancel", callback=self.cancel
        )
        self.add_item(cancelation_button)

    async def publish_rule(self, interaction: discord.Interaction):
        guild = interaction.client.database.find_guild(guild_id=interaction.guild.id)
        reglement_channel_id = guild.reglement_channel_id
        if not reglement_channel_id:
            raise Exception("No reglement channel specified")
        channel = interaction.guild.get_channel(reglement_channel_id)
        if not channel:
            raise Exception("Invalid channel id")
        embed = Embed(description=f"### Règlement du serveur")
        for rule in guild.rules:
            if rule.title:
                name = f"{rule.title}"
            else:
                name = ""
            embed.add_field(
                name=name,
                value=rule.content,
                inline=False,
            )
            reglement_message_id = guild.reglement_message_id
            if not reglement_message_id:
                raise Exception("No reglement message specified")
            reglement_message = await channel.fetch_message(reglement_message_id)
            if not reglement_message:
                raise Exception("Invalid message id")
            try:
                print("3")
                await reglement_message.edit(embed=embed)
                await channel.send(
                    f"<@&1245440658987028602>, La règle {rule.title} - {rule.content} a été modifiée"
                )
                embed = Embed(
                    description=f"La règle {rule.title} - {rule.content} a été publiée"
                )
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)

    async def cancel(self, interaction: discord.Interaction):
        embed = Embed(description=f"La règle n'a pas été publiée")
        await interaction.response.send_message(embed=embed)
