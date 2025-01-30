from fastapi import APIRouter, HTTPException, Query, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from DAL.schemas import City, CityForecastRequest
from .dependencies import weather_service
from typing import List, Literal
from datetime import datetime, date
from DAL.exceptions import ObjectNotFoundException
from BLL.exceptions import HttpClientException
import re

main_router = APIRouter()

@main_router.get("/weather", status_code=status.HTTP_200_OK)
async def get_current_weather(
    latitude: float = Query(None, description="Широта"),
    longitude: float = Query(None, description="Долгота")
):
    try:
        return await weather_service.get_current_weather_by_coordinates(latitude=latitude, longitude=longitude)
    except HttpClientException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    

@main_router.put(
    "/cities/{city}",
    summary="Метод для добавления отслеживаемых городов",
    description=
        '''Принимает название города и его координаты
        и добавляет в список городов для которых отслеживается прогноз погоды
        ''',
    status_code=status.HTTP_201_CREATED
)
async def add_city(
    city: str = Path(..., description="Название города латиницей")
):
    if not re.fullmatch(r"^[a-zA-Z\s-]+$", city):
        raise HTTPException(status_code=400, detail="Название города должно быть написано латиницей")
    try:
        await weather_service.add_city_to_tracking(City(name=city))
        return {"message": "Прогноз города успешно отслеживается"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")
    

@main_router.get(
    "/cities/tracked",
    status_code=status.HTTP_200_OK
)
async def get_all_tracked_cities():
    try:
        return await weather_service.get_tracked_cities()
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")


@main_router.get(
    "/cities/{city}/forecast/{time}",
    status_code=status.HTTP_200_OK
)
async def get_city_forecast(
    city: str = Path(..., description="Название города латиницей"),
    time: str = Path(..., description="Время в формате 'HH:MM' (24-часовой формат)"),
    weather_parameters: List[Literal["temperature", "humidity", "wind_speed", "precipitation", "pressure"]] = Query(
        default=["temperature", "humidity", "wind_speed", "precipitation", "pressure"],
        description="Список параметров погоды, которые нужно получить. Возможные значения: temperature, humidity, wind_speed, precipitation",
    )
):
    
    try:
        request = CityForecastRequest(
            name=city, 
            timestamp=datetime.combine(date.today(), datetime.strptime(time, "%H:%M").time()), 
            params=weather_parameters
            )
        return await weather_service.get_city_forecast(request=request)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат времени")
    except ObjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except:
        raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")