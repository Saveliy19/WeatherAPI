from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

    weather_data = relationship("WeatherData", back_populates="city")

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(String)
    humidity = Column(String)
    wind_speed = Column(String)
    pressure = Column(String)
    precipitation = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
    
    city_id = Column(Integer, ForeignKey("cities.id"))
    
    city = relationship("City", back_populates="weather_data")
