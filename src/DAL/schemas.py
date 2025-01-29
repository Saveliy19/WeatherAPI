from pydantic import BaseModel
from typing import Optional
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