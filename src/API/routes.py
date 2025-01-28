from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from BLL.abstract.abstract_weather_service import IWeatherService
from BLL.weather_service import WeatherService
from DAL.abstract.abstract_repository import IRepository
from DAL.repository import Repository
from DAL.schemas import City
from DAL.database import get_db

main_router = APIRouter()

def get_city_repository() -> IRepository:
    return Repository()

def get_weather_service(repository: IRepository = Depends(get_city_repository)) -> IWeatherService:
    return WeatherService(repository=repository)

@main_router.put(
    "/tracked_cities/{city}",
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
    city: str,
    latitude: float = Query(None, description="Широта"),
    longitude: float = Query(None, description="Долгота"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    try:
        await weather_service.add_city_to_tracking(City(name=city, latitude=latitude, longitude=longitude))
    except:
        raise