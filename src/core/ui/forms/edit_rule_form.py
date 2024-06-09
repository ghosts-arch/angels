from discord import TextStyle
import discord
from discord.ui import Modal, TextInput

from src.core.client import Angels
from src.core.embeds import SuccessEmbed
from src.core.database.models import Rule


class EditRuleForm(Modal):

    def __init__(self, rule: Rule) -> None:
        super().__init__(title="Editer une règle")
        self.__rule = rule
        self.rule_title = TextInput(
            label="titre",
            style=TextStyle.short,
            placeholder=self.__rule.title,
            default=self.__rule.title,
            required=False,
            max_length=64,
        )

        self.rule_tag = TextInput(
            label="tag",
            style=TextStyle.short,
            placeholder="tag",
            default=self.__rule.tag,
            required=True,
            min_length=4,
            max_length=16,
        )

        self.rule_content = TextInput(
            label="Nouvelle règle",
            style=TextStyle.paragraph,
            # placeholder=self.__rule.content,
            default=self.__rule.content,
            min_length=4,
            max_length=256,
        )

        self.add_item(self.rule_title)
        self.add_item(self.rule_tag)
        self.add_item(self.rule_content)

    @property
    def rule(self) -> Rule:
        return self.__rule

    async def on_submit(self, interaction: discord.Interaction[Angels]):
        if not interaction.guild:
            raise Exception("This command can only be used in a guild")
        rule = interaction.client.database.edit_rule(
            guild_id=interaction.guild.id,
            rule_tag=self.rule.tag,
            title=self.rule_title.value,
            content=self.rule_content.value,
        )
        self.stop()
        if rule.title:
            name = f"{rule.title} (*tag : {rule.tag}*)"
        else:
            name = f"Règle sans titre (*tag : {rule.tag}*)"
        await interaction.response.send_message(
            embed=SuccessEmbed(title="La règle suivante à été modifiée").add_field(
                name=name, value=rule.content
            )
        )
