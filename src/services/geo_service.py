from abc import abstractmethod

from core.config import settings
from httpx import AsyncClient
from schemas.address import AddressDTO

from services import Service


class GeoService(Service):
    @abstractmethod
    async def clean_address(self, address: str) -> AddressDTO: ...


class GeoServiceImpl(GeoService):
    async def clean_address(self, address: str) -> AddressDTO:
        async with AsyncClient() as client:
            json_data: list[dict] = (
                await client.post(
                    url="https://cleaner.dadata.ru/api/v1/clean/address",
                    headers={
                        "Authorization": f"Token {settings.dadata.api_key}",
                        "X-Secret": settings.dadata.secret_key,
                    },
                    json=[address],
                )
            ).json()
            return AddressDTO(
                name=json_data[0]["result"],
                latitude=json_data[0]["geo_lat"],
                longitude=json_data[0]["geo_lon"],
            )
