# encode : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from src.core.interaction import Context, Interaction
from src.core.embeds import Embed


class ApplicationCommand(Interaction):

    def __init__(self) -> None:
        self.name = "servers"
        self.description = "Renvoie la liste des servers"
        self.adminstration_channel_only = True
        self.moderator_only = True
        self.hidden = True

    async def run(self, context: Context):
        for server in context.client.guilds:
            embed = Embed(title=server.name, description=f"{server.id}")
            await context.interaction.channel.send(embed=embed)
