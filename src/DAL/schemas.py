from pydantic import BaseModel
from typing import Optional

class City(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None