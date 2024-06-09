# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import io
import discord
import sqlalchemy
import os


from sqlalchemy import (
    and_,
    select,
)
from sqlalchemy.orm import sessionmaker

from .models import Base, Rule, Guild


class Database:

    def __init__(self):
        echo = bool(os.getenv("DEV_MODE"))
        self.engine = sqlalchemy.create_engine(
            "sqlite:///src/core/database/database.db",
            echo=echo,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)

    def create_guild(self, guild_id: int):
        with self.Session() as session:
            guild = Guild(guild_id=guild_id, member_role_id=None)
            session.add(guild)
            session.commit()
            return guild

    def find_guild(self, guild_id: int):
        with self.Session() as session:
            stmt = select(Guild).where(Guild.guild_id == guild_id)
            guild = session.scalars(statement=stmt).first()

            if not guild:
                raise Exception("This guild does not exists.")
            return guild

    """def get_all_reglement_messages_id(self):
        with self.Session() as session:
            stmt = select(Guild.reglement_message_id)
            return session.scalars(statement=stmt).all()"""

    def set_member_role(self, guild_id: int, role_id):
        with self.Session() as session:
            guild = self.find_guild(guild_id=guild_id)

            guild.set_member_role_id(role_id=role_id)

            session.add(guild)
            session.commit()

    def set_reglement_message_id(self, guild_id: int, message_id: int):
        with self.Session() as session:
            guild = self.find_guild(guild_id=guild_id)

            guild.set_reglement_message_id(message_id=message_id)

            session.add(guild)
            session.commit()

    def set_reglement_channel_id(self, guild_id: int, channel_id: int):
        with self.Session() as session:
            guild = self.find_guild(guild_id=guild_id)
            guild.set_reglement_channel_id(channel_id=channel_id)
            session.add(guild)
            session.commit()

    def get_rules(self, guild_id: int):
        with self.Session() as session:
            stmt = select(Rule).where(Rule.guild_id == guild_id)
            rules = session.scalars(statement=stmt).all()
        return rules

    def get_rule(self, guild_id: int, rule_id: int):
        with self.Session() as session:
            stmt = select(Rule).where(
                and_(Rule.id == rule_id, Rule.guild_id == guild_id)
            )
            rule = session.scalars(statement=stmt).first()
        return rule

    def add_rule(self, guild_id: int, title: str | None, tag: str, content: str):
        with self.Session() as session:
            rule = Rule(title=title, guild_id=guild_id, tag=tag, content=content)
            session.add(rule)
            session.commit()
            return rule

    def delete_rule(self, rule_id: int):
        with self.Session() as session:
            stmt = select(Rule).where(Rule.id == rule_id)
            rule = session.scalars(statement=stmt).first()
            if rule:
                session.delete(rule)
                session.commit()
                return rule
            else:
                raise Exception("Rule not found")

    def edit_rule(self, guild_id: int, rule_tag: str, title: str | None, content: str):
        with self.Session() as session:
            stmt = select(Rule).where(
                and_(Rule.tag == rule_tag, Rule.guild_id == guild_id)
            )
            rule = session.scalars(statement=stmt).first()
            if rule:
                rule.content = content
                rule.title = title
                session.add(rule)
                session.commit()
                return rule
            else:
                raise Exception("Rule not found")

    def send_database(self):
        with io.open("src/core/database/database.db", mode="rb") as f:
            return discord.File(f)
