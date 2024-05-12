# encode : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from src.core.interaction import Context, Interaction


class ApplicationCommand(Interaction):

    def __init__(self) -> None:
        self.name = "database"
        self.description = "Renvoie la base de données"
        self.adminstration_channel_only = True
        self.moderator_only = True
        self.hidden = True

    async def run(self, context: Context):
        database = context.client.database.send_database()
        await context.send(file=database)
