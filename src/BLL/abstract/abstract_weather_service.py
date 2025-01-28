from abc import ABC, abstractmethod
from typing import Type
from DAL.schemas import City
from DAL.abstract.abstract_repository import IRepository

class IWeatherService(ABC):

    def __init__(self, repository: Type[IRepository]):
        self.repository = repository

    @abstractmethod
    async def add_city_to_tracking(city: City):
        pass

    @abstractmethod
    async def fetch_weather(city: City):
        pass

    @abstractmethod
    async def get_tracked_cities():
        pass