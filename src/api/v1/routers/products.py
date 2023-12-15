from fastapi import APIRouter
from core.context import app_configuration
from schemas.product import ProductDTO
from schemas.request import QueryProductsRequest
from services.product_service import ProductService

router = APIRouter(tags=["products"])


@router.get(
    "/",
    response_model=list[ProductDTO],
    name="query_products",
)
async def query_products(
    query_products_request: QueryProductsRequest | None = None,
) -> list[ProductDTO]:
    if query_products_request is None:
        query_products_request = QueryProductsRequest()
    return await app_configuration.get_service(ProductService).query_products(
        query_products_request.text, query_products_request.category_slug
    )
