from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from schemas.submenu import SubmenuCreate, SubmenuDTO
from services.submenu_service import SubmenuService, submenu_service

router = APIRouter()


@router.get(
    "/all_parent", response_model=list[SubmenuDTO], name="get_all_parent_categories"
)
async def get_all_parent_categories(service: SubmenuService = Depends(submenu_service)):
    return await service.get_all_parent_categories()


@router.get(
    "/{category_slug}/subcategories",
    response_model=SubmenuDTO,
    name="get_all_subcategories",
)
async def get_all_subcategories(
    category_slug: str, service: SubmenuService = Depends(submenu_service)
):
    if not await service.get_category(category_slug):
        raise HTTPException(status_code=404, detail="category not found")
    return await service.get_all_subcategories()
