from .abstract.abstract_http_client import IHttpClient
from DAL.schemas import Request
from typing import Any
from aiohttp import ClientSession
from .exceptions import HttpClientException

class HttpClient(IHttpClient):
    async def get_data(self, request: Request) -> dict[str, Any]:
        async with ClientSession() as session:
            async with session.get(request.url, params=request.params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HttpClientException(status_code=response.status, message=error_text)
                
                return await response.json()