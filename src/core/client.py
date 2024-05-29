# encode : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import asyncio
import pathlib
import discord

import traceback


from src.core.embeds import ErrorEmbed
from .database.database import Database
from .interaction import (
    Context,
    load_application_commands,
    register_application_commands,
)
from src.core.ui.views import AcceptRulesView
from .config import load_config
from ..utils.logger import Logger


logger = Logger()

config_path = pathlib.Path("config.yaml")

intents = discord.Intents(members=True, guilds=True)


class Angels(discord.Client):

    def __init__(self):

        super().__init__(intents=intents)
        self.database = Database()
        self.application_commands = load_application_commands()
        self.config = load_config(path=config_path)
        self.cooldowns = []
        self.loop = asyncio.get_event_loop()

    async def on_ready(self):

        try:
            await register_application_commands(
                application_commands=self.application_commands
            )
        except Exception:
            logger.error(traceback.format_exc())

        """reglements_messages_id = self.database.get_all_reglement_messages_id()
        for reglement_message_id in reglements_messages_id:
            self.add_view(AcceptRulesView(), message_id=reglement_message_id)"""
        logger.info(f"Logged as {self.user}")
        test_channel = self.get_channel(self.config.get("TEST_CHANNEL_ID"))

        if isinstance(test_channel, discord.TextChannel):
            await test_channel.send(f"{self.user} ready.")

    async def on_guild_join(self, guild: discord.Guild):
        self.database.create_guild(guild_id=guild.id)
        logger.info(f"Joined guild {guild.name}")

    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type == discord.InteractionType.application_command:
            context = Context(interaction)
            command = self.application_commands.get(context.name)

            if not command:
                return

            if not context.guild:
                return

            if not context.channel:
                return

            if not isinstance(context.user, discord.Member):
                return

            if (
                command.run_by_moderator_only()
                and not context.user.guild_permissions.administrator
            ):
                await context.send(
                    embed=ErrorEmbed(
                        description="This command can only be used by moderators."
                    )
                )
                return

            try:
                await command.run(context=context)
            except Exception as error:
                await interaction.response.send_message(
                    embed=ErrorEmbed(
                        description=traceback.format_exc(),
                    )
                )
