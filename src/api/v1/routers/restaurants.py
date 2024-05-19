from uuid import UUID
from fastapi import APIRouter, HTTPException
from schemas.restaurant import RestaurantDB, RestaurantDTO
from core.context import app_configuration
from services.restaurant_service import RestaurantService

router = APIRouter(tags=["restaurants"])


@router.get(
    "/city/{city_id}",
    response_model=list[RestaurantDB],
    name="Get city restaurants",
)
async def get_city_restaurants(city_id: UUID) -> list[RestaurantDB]:
    return await app_configuration.get_service(RestaurantService).get_city_restaurants(
        str(city_id)
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantDTO,
    name="Get restaurant by id",
)
async def get_restaurant(restaurant_id: UUID) -> RestaurantDTO:
    if restaurant := await app_configuration.get_service(
        RestaurantService
    ).get_restaurant(str(restaurant_id)):
        return restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found")


@router.get(
    "/admin/{admin_user_id}",
    response_model=list[RestaurantDB],
    name="Get admin restaurants",
)
async def get_admin_restaurants(admin_user_id: UUID) -> list[RestaurantDB]:
    return await app_configuration.get_service(RestaurantService).get_admin_restaurants(
        str(admin_user_id)
    )
