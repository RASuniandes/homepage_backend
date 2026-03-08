"""
Example model — replace / extend with your own domain models.

Demonstrates: mapped_column, TimestampMixin, and relationship patterns.
"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class Item(Base, TimestampMixin):
    """A minimal example entity."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name!r}>"
