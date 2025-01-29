from .abstract.abstract_repository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import City as dbCity, WeatherData
from .schemas import City as dtoCity, HourlyForecast as dtoForecast
from .database import get_db
from typing import List


class Repository(IRepository):

    async def add_city_to_tracking(self, city: dtoCity):
        async with get_db() as session:
            db_city = dbCity(name=city.name, latitude=city.latitude, longitude=city.longitude)
            session.add(db_city)
            await session.commit()

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