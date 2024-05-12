# coding : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

from typing import Optional
from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite


class Base(DeclarativeBase):
    pass


class Rule(Base):
    __tablename__ = "rule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(
        ForeignKey("guild.guild_id"), nullable=False, unique=True
    )
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    tag: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    guild: Mapped["Guild"] = relationship(back_populates="rules")


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(nullable=False)
    rules: Mapped["Rule"] = relationship(back_populates="guild", lazy="selectin")
