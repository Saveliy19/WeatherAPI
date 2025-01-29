from BLL.abstract.abstract_weather_service import IWeatherService
from BLL.abstract.abstract_http_client import IHttpClient
from BLL.http_client import HttpClient
from BLL.weather_service import WeatherService
from DAL.abstract.abstract_repository import IRepository
from DAL.repository import Repository

repository: IRepository = Repository()
http_client: IHttpClient = HttpClient()
weather_service: IWeatherService = WeatherService(
    repository=repository,
    http_client=http_client
)