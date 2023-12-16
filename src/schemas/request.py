from pydantic import BaseModel


class QueryProductsRequest(BaseModel):
    text: str = ""
    category_slug: str = ""
