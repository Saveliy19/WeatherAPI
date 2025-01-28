from .abstract.abstract_repository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import City as dbCity, WeatherData
from .schemas import City as dtoCity, CurrentWeather as dtoForecast
from .database import get_db


class Repository(IRepository):

    async def add_city_to_tracking(self, city: dtoCity):
        session = await get_db().__anext__()

        try:
            db_city = dbCity(name=city.name, latitude=city.latitude, longitude=city.longitude)
            session.add(db_city)
            await session.commit()
        finally:
            await session.close()

    async def get_tracked_cities(self):
        session = await get_db().__anext__()

        try:
            result = await session.execute(select(dbCity))
            cities = result.scalars().all()
            return [dtoCity(name=city.name, latitude=city.latitude, longitude=city.longitude) for city in cities]
        finally:
            await session.close()

    async def update_weather_forecast(city: dtoCity, forecast: dtoForecast):
        session = await get_db().__anext__()
        pass