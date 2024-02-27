from uuid import UUID

from core.auth import get_user
from core.context import app_configuration
from fastapi import APIRouter, Depends
from schemas.address import AddressDTO, AddressRequest, DeliveryAddressDTO
from schemas.user import User
from services.address_service import AddressService

router = APIRouter(tags=["addresses"])


@router.post(
    "/clean-address",
    name="clean-address",
)
async def clean_address(
    address_request: AddressRequest, _: User = Depends(get_user)
) -> AddressDTO:
    return await app_configuration.get_service(AddressService).clean_address(
        address_request.address
    )


@router.get("/delivery-addresses", name="Get delivery addresses")
async def get_delivery_addresses(
    user: User = Depends(get_user),
) -> list[DeliveryAddressDTO]:
    return await app_configuration.get_service(AddressService).get_delivery_addresses(
        user.id
    )


@router.post(
    "/delivery-addresses",
    name="Add delivery address",
)
async def add_delivery_address(
    address: AddressDTO, user: User = Depends(get_user)
) -> None:
    await app_configuration.get_service(AddressService).add_delivery_address(
        address, user.id
    )


@router.delete(
    "/delivery-addresses/{address_id}",
    name="Delete delivery address",
)
async def delete_delivery_address(
    address_id: UUID, user: User = Depends(get_user)
) -> None:
    await app_configuration.get_service(AddressService).delete_delivery_address(
        address_id, user.id
    )
