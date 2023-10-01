from __future__ import annotations
import uuid
import strawberry
from uuid import uuid4


@strawberry.type
class Category:
    id: uuid.UUID
    title: str
    description: str | None
    products: list[Product | None] | None
    parent: Category | None


@strawberry.type
class Product:
    id: uuid.UUID
    title: str
    description: str | None
    price: float
    category: Category | None


category_id1 = uuid4()
category_id2 = uuid4()

categories = [
    Category(
        id=category_id1,
        title="Category 1",
        description="Category 1 description",
        products=[
            Product(
                id=uuid4(),
                title="Product 1",
                description="Product 1 description",
                price=10.0,
                category=None,
            ),
            Product(
                id=uuid4(),
                title="Product 2",
                description="Product 2 description",
                price=20.0,
                category=None,
            ),
        ],
        parent=None,
    ),
    Category(
        id=category_id2,
        title="Category 2",
        description="Category 2 description",
        products=[
            Product(
                id=uuid4(),
                title="Product 1",
                description="Product 1 description",
                price=10.0,
                category=None,
            ),
            Product(
                id=uuid4(),
                title="Product 2",
                description="Product 2 description",
                price=20.0,
                category=None,
            ),
        ],
        parent=None,
    ),
]


def get_categories() -> list[Category]:
    return categories


@strawberry.type
class Query:
    @strawberry.field
    def categories(self, id: uuid.UUID | None = None) -> list[Category]:
        if id:
            return [category for category in categories if category.id == id]
        return categories


schema = strawberry.Schema(query=Query)
