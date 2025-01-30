from .abstract.abstract_repository import IRepository
from sqlalchemy.future import select
from .models import City as dbCity, WeatherData
from .schemas import City as dtoCity, HourlyForecast as dtoForecast, CityForecastRequest, CityForecastResponse
from .database import get_db
from typing import List
from .exceptions import ObjectNotFoundException


class Repository(IRepository):

    async def add_city_to_tracking(self, city: dtoCity) -> dtoCity:
        async with get_db() as session:
            db_city = dbCity(name=city.name, latitude=city.latitude, longitude=city.longitude)
            session.add(db_city)
            await session.commit()
            await session.refresh(db_city)
            city.id = db_city.id
            return city

    async def get_tracked_cities(self):
        async with get_db() as session:
            result = await session.execute(select(dbCity))
            cities = result.scalars().all()
            return [dtoCity(id=city.id, name=city.name, latitude=city.latitude, longitude=city.longitude) for city in cities]

    async def update_weather_forecast(self, city: dtoCity, forecast: List[dtoForecast]):
        async with get_db() as session:
            for data in forecast:
                weather_entry = WeatherData(
                    temperature=data.temperature,
                    wind_speed=data.wind_speed,
                    pressure=data.atmospheric_pressure,
                    precipitation=data.precipitation,
                    humidity=data.humidity,
                    timestamp=data.timestamp,
                    city_id=city.id
                )

                existing_entry = await session.execute(
                    select(WeatherData).filter_by(
                        city_id=city.id,
                        timestamp=data.timestamp
                    )
                )
                existing_entry = existing_entry.scalar_one_or_none()

                if existing_entry:
                    existing_entry.temperature = weather_entry.temperature
                    existing_entry.wind_speed = weather_entry.wind_speed
                    existing_entry.pressure = weather_entry.pressure
                    existing_entry.precipitation = weather_entry.precipitation
                    existing_entry.humidity = weather_entry.humidity
                else:
                    session.add(weather_entry)

            await session.commit()

    async def get_city_forecast(self, request: CityForecastRequest) -> CityForecastResponse:
        async with get_db() as session:
            city = await session.execute(select(dbCity).filter(dbCity.name == request.name))
            city = city.scalar_one_or_none()

            if not city:
                raise ObjectNotFoundException(f"Город с названием {request.name} не найден в базе данных.")

            query = select(WeatherData).filter(
                WeatherData.city_id == city.id,
                WeatherData.timestamp <= request.timestamp
            ).order_by(WeatherData.timestamp.asc())

            result = await session.execute(query)
            weather_data = result.scalars().all()

            forecast = CityForecastResponse(city_name=request.name)
            params = request.params
            for data in weather_data:
                if 'temperature' in params:
                    forecast.temperature = data.temperature
                if 'humidity' in params:
                    forecast.humidity = data.humidity
                if 'wind_speed' in params:
                    forecast.wind_speed = data.wind_speed
                if 'precipitation' in params:
                    forecast.precipitation = data.precipitation
                if 'pressure' in request.params:
                    forecast.atmospheric_pressure = data.pressure

            return forecast