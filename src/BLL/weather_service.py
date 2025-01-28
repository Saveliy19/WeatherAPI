from .abstract.abstract_weather_service import IWeatherService
from DAL.schemas import City
from typing import List
import aiohttp
from fastapi import HTTPException

class WeatherService(IWeatherService):

    async def get_tracked_cities(self) -> List[City]:
        return await self.repository.get_tracked_cities()


    async def __is_city_tracked(self, city: City) -> bool:
        tracked_cities = await self.get_tracked_cities()

        for tracked_city in tracked_cities:
            if city.name == tracked_city.name:
                if tracked_city.latitude == city.latitude and tracked_city.longitude == city.longitude:
                    return True
        return False

    async def __get_default_coordinates(self, city: City) -> City:
        async with aiohttp.ClientSession() as session:
            url = f"https://geocode.maps.co/search?q={city.name}"
            
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Ошибка запроса: {response.status}")

                data = await response.json()

                if not data:
                    raise ValueError(f"Город {city.name} не найден")

                city.latitude = float(data[0]["lat"])
                city.longitude = float(data[0]["lon"])

        return city
    
    async def __validate_city_name(self, city: City):
        async with aiohttp.ClientSession() as session:
            url = f"https://geocode.maps.co/reverse?lat={city.latitude}&lon={city.longitude}"

            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail=f"Ошибка запроса: {response.status}")

                data = await response.json()

                if "display_name" not in data:
                    raise HTTPException(status_code=404, detail="Не удалось получить данные о местоположении")

                api_city_name = data["address"].get("city") or data["address"].get("town") or data["address"].get("village")

                if api_city_name.lower() != city.name.lower():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Название города {city.name} не соответствует координатам ({api_city_name})"
                    )

    async def add_city_to_tracking(self, city: City):
        if city.longitude is None or city.latitude is None:
            city = await self.__get_default_coordinates(city)

        else:
            await self.__validate_city_name(city) 

        if await self.__is_city_tracked(city):
            return

        await self.repository.add_city_to_tracking(city)

        
    async def fetch_weather(self, city: City):
        tracked_cities = self.repository.get_tracked_cities()

        for city in tracked_cities:
            pass