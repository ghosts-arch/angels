import discord
import discord.types
import discord.types.snowflake


from src.core.ui.views import DeleteRuleView

from src.core.ui.buttons import ConfirmationButton, CancelationButton
from src.core.ui.forms import AddRuleForm, EditRuleForm
from src.core.embeds import ErrorEmbed, SuccessEmbed, Embed
from src.core.interaction import Interaction, Context


class ApplicationCommand(Interaction):
    def __init__(self) -> None:
        self.name = "reglement"
        self.description = "Reglement du serveur"
        self.moderator_only = True
        self.options = [
            {
                "name": "afficher",
                "description": "Affiche le reglement du serveur",
                "type": 1,
                "options": [
                    {
                        "name": "channel",
                        "description": "Salon d'affichage du reglement",
                        "type": 7,
                        "required": False,
                    }
                ],
            },
            {
                "name": "ajouter",
                "description": "Ajouter une règle",
                "type": 1,
            },
            {
                "name": "modifier",
                "description": "modifier une règle",
                "type": 1,
                "options": [
                    {
                        "name": "tag",
                        "description": "tag de la règle à modifier",
                        "type": 3,
                        "required": True,
                    },
                ],
            },
            {
                "name": "supprimer",
                "description": "Supprimer une règle",
                "type": 1,
                "options": [
                    {
                        "name": "tag",
                        "description": "tag de la règle à supprimer",
                        "type": 3,
                        "required": True,
                    }
                ],
            },
        ]

    async def run(self, context: Context):
        if not context.guild:
            raise Exception("This command can only be used in a guild")
        subcommand = context.subcommand
        arguments = context.arguments
        match subcommand:
            case "afficher":
                rules = context.client.database.get_rules(context.guild.id)
                if not rules:
                    error_embed = ErrorEmbed(
                        description="Il n'y a pas de règles pour le moment. Vous pouvez ajouter une règle avec la commande </reglement ajouter:1231990212922445894>.",
                    )
                    return await context.send(embed=error_embed)
                embed = Embed(description=f"### Règlement du serveur")
                for rule in rules:
                    if rule.title:
                        name = f"{rule.title} (*tag : {rule.tag}*)"
                    else:
                        name = f"(*tag : {rule.tag}*)"
                    embed.add_field(
                        name=name,
                        value=rule.content,
                        inline=False,
                    )
                if not arguments:
                    return await context.send(embed=embed)
                else:
                    channel = arguments[0].get("value")
                    if not channel:
                        raise Exception("Invalid channel id")

                    return await context.send_in_channel(
                        channel_id=int(channel), embed=embed
                    )
            case "ajouter":
                add_rule_form = AddRuleForm()
                return await context.interaction.response.send_modal(add_rule_form)
            case "modifier":
                if not arguments:
                    raise Exception("You must specify the tag of the rule to edit.")
                rule_tag = arguments[0].get("value")
                if not rule_tag:
                    raise Exception("You must specify the tag of the rule to edit.")
                if not type(rule_tag) == str:
                    raise Exception("The rule tag must be an str.")
                rule = context.client.database.get_rule(
                    guild_id=context.guild.id, rule_tag=rule_tag
                )
                if not rule:
                    raise Exception("The rule does not exist.")
                edit_rule_form = EditRuleForm(rule=rule)
                return await context.interaction.response.send_modal(edit_rule_form)
            case "supprimer":
                if not arguments:
                    raise Exception("You must specify the tag of the rule to delete.")
                rule_tag = arguments[0].get("value")
                if not rule_tag:
                    raise Exception("You must specify the tag of the rule to delete.")
                if type(rule_tag) != str:
                    raise Exception("The rule tag must be an string.")
                rule = context.client.database.get_rule(
                    guild_id=context.guild.id, rule_tag=rule_tag
                )
                if not rule:
                    error_embed = ErrorEmbed(
                        description="Cette règle n'existe pas.",
                    )
                    return await context.send(embed=error_embed)
                embed = Embed(
                    title="Confirmation",
                    description=f"Êtes-vous sûr de vouloir supprimer la règle (*tag : {rule.tag}*)?",
                )
                view = DeleteRuleView(rule=rule)

                await context.interaction.response.send_message(embed=embed, view=view)

            case _:
                raise Exception("Unknown subcommand.")
