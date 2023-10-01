import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import BaseModel

if TYPE_CHECKING:
    from models import Good


class Category(BaseModel):
    __tablename__: str = 'category'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    goods: Mapped[list["Good"]] = relationship(
        'Good', back_populates='category', cascade='all, delete-orphan'
    )
