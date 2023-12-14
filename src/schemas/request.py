from pydantic import BaseModel


class QueryProductsRequest(BaseModel):
    text: str | None = None
    category_slug: str | None = None
