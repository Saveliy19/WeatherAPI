from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class City(BaseModel):
    name: str
    id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CurrentWeather(BaseModel):
    temperature: str
    wind_speed: str
    atmospheric_pressure: str
    
class HourlyForecast(CurrentWeather):
    precipitation: str
    humidity: str
    timestamp: datetime

class Request(BaseModel):
    params: Optional[dict] = {}
    url: str

class CityForecastRequest(BaseModel):
    name: str
    timestamp: datetime
    params: List[str]

class CityForecastResponse(BaseModel):
    city_name: str
    temperature: Optional[str] = None
    wind_speed: Optional[str] = None
    atmospheric_pressure: Optional[str] = None
    precipitation: Optional[str] = None
    humidity: Optional[str] = None