from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_user
from schemas.category import CategoryDTO
from services.category_service import CategoryService
from core.context import app_configuration

router = APIRouter(tags=["categories"])


@router.get(
    "/all_parent",
    response_model=list[CategoryDTO],
    name="get_all_parent_categories",
)
async def get_all_parent_categories(user=Depends(get_user)) -> list[CategoryDTO]:
    return await app_configuration.get_service(
        CategoryService
    ).get_all_parent_categories()


@router.get(
    "/{category_slug}",
    response_model=CategoryDTO,
    name="get_all_subcategories",
)
async def get_subcategory(category_slug: str) -> CategoryDTO:
    if category := await app_configuration.get_service(CategoryService).get_category(
        category_slug
    ):
        return category
    raise HTTPException(status_code=404, detail="Category not found")
