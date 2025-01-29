from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from DAL.schemas import City, CityForecastRequest
from .dependencies import weather_service
from typing import List
from datetime import datetime, date
import re

main_router = APIRouter()

@main_router.get("/weather")
async def get_current_weather(
    latitude: float = Query(None, description="Широта"),
    longitude: float = Query(None, description="Долгота")
):
    try:
        return await weather_service.get_current_weather_by_coordinates(latitude=latitude, longitude=longitude)
    except:
        raise
    

@main_router.put(
    "/cities/{city}",
    responses={
        200: {"description": "Город добавлен и отслеживается"},
        400: {"description": "Некорректное имя города или координаты"}
    },
    summary="Метод для добавления отслеживаемых городов",
    description=
        '''Принимает название города и его координаты
        и добавляет в список городов для которых отслеживается прогноз погоды
    '''
)
async def add_city(
    city: str = Path(..., description="Название города латиницей")
):
    if not re.fullmatch(r"^[a-zA-Z\s-]+$", city):
        raise HTTPException(status_code=400, detail="Название города должно быть написано латиницей")
    try:
        await weather_service.add_city_to_tracking(City(name=city))
    except:
        raise

@main_router.get(
    "/cities/tracked"
)
async def get_all_tracked_cities():
    try:
        return await weather_service.get_tracked_cities()
    except:
        raise

@main_router.get(
    "/cities/{city}/forecast/{time}",

)
async def get_city_forecast(
    city: str = Path(..., description="Название города латиницей"),
    time: str = Path(..., description="Время в формате 'HH:MM' (24-часовой формат)"),
    weather_parameters: List[str] = Query(
        default=["temperature", "humidity", "wind_speed", "precipitation", "pressure"],
        description="Список параметров погоды, которые нужно получить. Возможные значения: temperature, humidity, wind_speed, precipitation"
    )
):
    request = CityForecastRequest(name=city, timestamp=datetime.combine(date.today(), datetime.strptime(time, "%H:%M").time()), params=weather_parameters)
    try:
        return await weather_service.get_city_forecast(request=request)
    except:
        raise