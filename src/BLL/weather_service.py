from .abstract.abstract_weather_service import IWeatherService
from DAL.schemas import City, CurrentWeather, Request, HourlyForecast, CityForecastRequest, CityForecastResponse
from typing import List
import aiohttp
from .abstract.abstract_http_client import IHttpClient
import asyncio

class WeatherService(IWeatherService):
    async def get_tracked_cities(self) -> List[City]:
        return await self.repository.get_tracked_cities()


    async def __is_city_tracked(self, city: City) -> bool:
        tracked_cities = await self.get_tracked_cities()

        for tracked_city in tracked_cities:
            if city.name == tracked_city.name:
                return True
        return False

    async def __get_default_coordinates(self, city: City) -> City:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city.name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        request = Request(url=url, params=params)
        data = await self.http_client.get_data(request)

        if "results" in data and data["results"]:
            city.latitude = float(data["results"][0]["latitude"])
            city.longitude = float(data["results"][0]["longitude"])
            return city

        raise ValueError(f"Не удалось найти координаты для города: {city.name}")

    async def get_current_weather_by_coordinates(self, latitude: float, longitude: float) -> CurrentWeather:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,surface_pressure,wind_speed_10m"
        }

        request = Request(params=params, url=url)
        
        try:       
            data = await self.http_client.get_data(request=request)
        except:
            raise
        current_weather_data = data.get("current")
        current_weather_units = data.get("current_units")

        print(current_weather_data)
        weather = CurrentWeather(
            temperature=str(current_weather_data.get("temperature_2m")) + current_weather_units.get("temperature_2m"),
            wind_speed=str(current_weather_data.get("wind_speed_10m")) + current_weather_units.get("wind_speed_10m"),
            atmospheric_pressure=str(current_weather_data.get("surface_pressure")) + current_weather_units.get("surface_pressure")
        )
        return weather

    async def add_city_to_tracking(self, city: City):
        city = await self.__get_default_coordinates(city)

        if await self.__is_city_tracked(city):
            return

        city = await self.repository.add_city_to_tracking(city)
        forecast = await self.__get_hourly_forecast(city)
        await self.repository.update_weather_forecast(city, forecast)

    async def __get_hourly_forecast(self, city: City) -> List[HourlyForecast]:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "hourly" : "temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m",
            "timezone" : "Europe/Moscow",
            "forecast_days": 1
        }
        request = Request(params=params, url=url)

        data = await self.http_client.get_data(request=request)
        hourly_weather_data = data.get("hourly")
        weather_units = data.get("hourly_units")

        forecast: List[HourlyForecast] = []

        for i in range(len(hourly_weather_data.get("time"))):
            forecast.append(
                HourlyForecast(
                    temperature=str(hourly_weather_data.get("temperature_2m")[i]) + weather_units.get("temperature_2m"),
                    humidity=str(hourly_weather_data.get("relative_humidity_2m")[i]) + weather_units.get("relative_humidity_2m"),
                    precipitation=str(hourly_weather_data.get("precipitation")[i]) + weather_units.get("precipitation"),
                    atmospheric_pressure=str(hourly_weather_data.get("surface_pressure")[i]) + weather_units.get("surface_pressure"),
                    wind_speed=str(hourly_weather_data.get("wind_speed_10m")[i]) + weather_units.get("wind_speed_10m"),
                    timestamp=hourly_weather_data.get("time")[i]
                )
            )
        return forecast

        
    async def update_all_forecasts(self):
        while True:
            tracked_cities = await self.repository.get_tracked_cities()
            for city in tracked_cities:
                forecast = await self.__get_hourly_forecast(city)
                await self.repository.update_weather_forecast(city, forecast)
            print("Данные обновлены!")
            await asyncio.sleep(15*60)

    async def get_city_forecast(self, request: CityForecastRequest) -> CityForecastResponse:
        return await self.repository.get_city_forecast(request=request)