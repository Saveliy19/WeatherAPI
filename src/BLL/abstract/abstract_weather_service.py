from abc import ABC, abstractmethod
from typing import Type, List
from DAL.schemas import City, CurrentWeather
from DAL.abstract.abstract_repository import IRepository

class IWeatherService(ABC):

    def __init__(self, repository: Type[IRepository]):
        self.repository = repository

    @abstractmethod
    async def add_city_to_tracking(self, city: City):
        pass

    @abstractmethod
    async def fetch_weather(self, city: City):
        pass

    @abstractmethod
    async def get_tracked_cities(self) -> List[City]:
        pass

    @abstractmethod
    async def get_current_weather_by_coordinates(self, latitude: float, longitude: float) -> CurrentWeather:
        pass