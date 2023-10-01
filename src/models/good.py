import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import BaseModel

if TYPE_CHECKING:
    from models import Category


class Good(BaseModel):
    __tablename__: str = 'good'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('category.id', ondelete='CASCADE')
    )
    category: Mapped["Category"] = relationship('Category', back_populates='goods')
