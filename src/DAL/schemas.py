from pydantic import BaseModel
from typing import Optional

class City(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CurrentWeather(BaseModel):
    temperature: str
    wind_speed: str
    atmospheric_pressure: str
    precipitation: str
    humidity: str