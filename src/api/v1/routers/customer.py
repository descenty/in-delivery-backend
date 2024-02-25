from typing import Optional
from uuid import UUID

from core.auth import get_user
from core.context import app_configuration
from fastapi import APIRouter, Depends
from schemas.customer import CustomerDTO
from schemas.user import User
from services.customer_service import CustomerService

router = APIRouter(tags=["customer"])


@router.get("/customer", name="get-customer-data")
async def get_customer_data(
    user: User = Depends(get_user),
) -> Optional[CustomerDTO]:
    return await app_configuration.get_service(CustomerService).get_customer_data(
        user.id
    )


@router.put("/delivery-addresses/{address_id}", name="select-delivery-address")
async def select_delivery_address(
    address_id: UUID, user: User = Depends(get_user)
) -> Optional[CustomerDTO]:
    return await app_configuration.get_service(CustomerService).select_delivery_address(
        address_id, user.id
    )
