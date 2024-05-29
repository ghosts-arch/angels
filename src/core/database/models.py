# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite


class Base(DeclarativeBase):
    pass


class Rule(Base):
    __tablename__ = "rule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guild.guild_id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    tag: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    guild: Mapped["Guild"] = relationship(back_populates="rules")


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    reglement_channel_id: Mapped[Optional[int]] = mapped_column()
    reglement_message_id: Mapped[Optional[int]] = mapped_column()
    member_role_id: Mapped[Optional[int]] = mapped_column()
    rules: Mapped[List["Rule"]] = relationship(
        back_populates="guild", lazy="selectin", uselist=True
    )

    def get_member_role_id(self):
        return self.member_role_id

    def set_member_role_id(self, role_id):
        self.member_role_id = role_id

    def set_reglement_channel_id(self, channel_id):
        self.reglement_channel_id = channel_id

    def set_reglement_message_id(self, message_id):
        self.reglement_message_id = message_id
