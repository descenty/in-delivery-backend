from fastapi import APIRouter, Depends
from core.auth import get_user
from core.context import app_configuration
from schemas.address import AddressDTO, AddressRequest
from schemas.user import User
from services.geo_service import GeoService

router = APIRouter(tags=["geo"])


@router.post(
    "/clean-address",
    name="clean-address",
)
async def add_product_to_cart(
    address_request: AddressRequest, _: User = Depends(get_user)
) -> AddressDTO:
    return await app_configuration.get_service(GeoService).clean_address(
        address_request.address
    )
