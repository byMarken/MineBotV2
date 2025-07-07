from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, String
from typing import Optional


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    minecraft_nick: Mapped[str] = mapped_column()
    balance: Mapped[int] = mapped_column(default=0)
    fake_balance: Mapped[int] = mapped_column(default=0)


class PendingAuthorization(Base):
    __tablename__ = "pending_authorizations"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    unique_amount: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    minecraft_nick: Mapped[Optional[str]] = mapped_column(String, nullable=True)
