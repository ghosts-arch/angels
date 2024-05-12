from src.core.embeds import Embed
from src.core.interaction import Interaction, Context


class ApplicationCommand(Interaction):
    def __init__(self) -> None:
        self.name = "aide"
        self.description = "Aide a propos des commandes"

    async def run(self, context: Context):
        commands = context.client.application_commands
        embed = Embed()
        for command_name, command in commands.items():
            if command.hidden:
                continue
            embed.add_field(
                name=f"Commande : {command_name}",
                value=command.get_description(),
                inline=False,
            )

        await context.send(embed=embed)
