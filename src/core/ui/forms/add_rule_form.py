from discord import TextStyle
import discord
import re
from discord.ui import Modal, TextInput

from src.core.embeds import SuccessEmbed
from src.core.client import Angels


class AddRuleForm(Modal):

    def __init__(self) -> None:
        super().__init__(title="Ajouter une règle")

        self.rule_title = TextInput(
            label="titre",
            style=TextStyle.short,
            placeholder="titre",
            required=False,
            max_length=64,
        )

        self.rule_tag = TextInput(
            label="tag",
            style=TextStyle.short,
            placeholder="tag",
            required=True,
            min_length=4,
            max_length=16,
        )

        self.rule_content = TextInput(
            label="Nouvelle règle",
            style=TextStyle.paragraph,
            placeholder="contenu",
            min_length=4,
            max_length=256,
        )

        self.add_item(self.rule_title)
        self.add_item(self.rule_tag)
        self.add_item(self.rule_content)

    async def on_submit(self, interaction: discord.Interaction[Angels]):
        if not interaction.guild:
            raise Exception("This command can only be used in a guild")
        print(interaction.guild.id)
        tag = format_tag(self.rule_tag.value)
        rule = interaction.client.database.add_rule(
            guild_id=interaction.guild.id,
            title=self.rule_title.value,
            tag=tag,
            content=self.rule_content.value,
        )
        self.stop()
        if rule.title:
            name = f"{rule.title} (*tag : {rule.tag}*)"
        else:
            name = f"Règle sans titre (*tag : {rule.tag}*)"
        embed = SuccessEmbed(title="La règle suivante à été ajoutée").add_field(
            name=name, value=rule.content
        )
        await interaction.response.send_message(embed=embed)


def format_tag(tag: str):

    # print(re.sub(r"[^\d\w]", "", tag))
    return re.sub(r"[^\d\w]", " ", tag).lower()
