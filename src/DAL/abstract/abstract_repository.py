from abc import ABC, abstractmethod
from typing import List
from DAL.schemas import City

class IRepository(ABC):
    
    @abstractmethod
    async def add_city_to_tracking(city: City):
        pass

    @abstractmethod
    async def get_tracked_cities() -> List[City]:
        pass