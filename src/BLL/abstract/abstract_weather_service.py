from abc import ABC, abstractmethod
from typing import List
from DAL.schemas import City, CurrentWeather, CityForecastRequest
from DAL.abstract.abstract_repository import IRepository
from .abstract_http_client import IHttpClient

class IWeatherService(ABC):

    def __init__(self, repository: IRepository, http_client: IHttpClient):
        self.repository = repository
        self.http_client = http_client

    @abstractmethod
    async def add_city_to_tracking(self, city: City):
        pass

    @abstractmethod
    async def update_all_forecasts(self):
        pass

    @abstractmethod
    async def get_tracked_cities(self) -> List[City]:
        pass

    @abstractmethod
    async def get_current_weather_by_coordinates(self, latitude: float, longitude: float) -> CurrentWeather:
        pass

    @abstractmethod
    async def get_city_forecast(self, request: CityForecastRequest):
        pass