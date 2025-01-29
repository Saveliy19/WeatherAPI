from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from DAL.schemas import City
from .dependencies import weather_service
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
    "/cities/tracked/{city}",
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
    city: str = Path(..., description="Название города на английском"),
    latitude: float = Query(None, description="Широта"),
    longitude: float = Query(None, description="Долгота")
):
    if not re.match(r'^[a-zA-Z\s]+$', city):
        raise HTTPException(status_code=400, detail="City name must only contain English letters")
    try:
        await weather_service.add_city_to_tracking(City(name=city, latitude=latitude, longitude=longitude))
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