from abc import ABC, abstractmethod
from DAL.schemas import Request
from typing import Any

class IHttpClient(ABC):
    @abstractmethod
    async def get_data(self, request: Request) -> dict[str, Any]:
        pass