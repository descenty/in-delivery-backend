from fastapi import APIRouter, HTTPException
from schemas.category import ParentCategoryDTO, CategoryCascadeDTO
from services.category_service import CategoryService
from core.context import app_configuration

router = APIRouter(tags=["categories"])


@router.get(
    "/all_parent",
    response_model=list[ParentCategoryDTO],
    name="get_all_parent_categories",
)
async def get_all_parent_categories() -> list[ParentCategoryDTO]:
    return await app_configuration.get_service(
        CategoryService
    ).get_all_parent_categories()


@router.get(
    "/{category_slug}",
    response_model=CategoryCascadeDTO,
    name="get_category",
)
async def get_category(category_slug: str) -> CategoryCascadeDTO:
    if category := await app_configuration.get_service(CategoryService).get_category(
        category_slug
    ):
        return category
    raise HTTPException(status_code=404, detail="Category not found")
