from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


# The class `Base` is an abstract class with an `id` attribute that is a mapped column with a primary
# key.
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class User(Base):

    telegram_id: Mapped[str] = mapped_column(unique=True)
    status_polic: Mapped[bool | None]
    time_reg: Mapped[datetime | None] = mapped_column(DateTime, default=func.now())
    last_strategy_id: Mapped[int | None]
    last_strategy_time: Mapped[datetime | None]


class Panel(Base):
    __tablename__ = "panel"

    glob_promo: Mapped[str | None]


class Strategy(Base):

    pool_strateg: Mapped[str] = mapped_column(unique=True)
