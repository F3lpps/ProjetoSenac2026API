from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@mapped_as_dataclass(table_registry)
class Story:
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    author: Mapped[str]
    title: Mapped[str]
    email: Mapped[str] = mapped_column(ForeignKey("user.email"), init=False)
    story: str
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
