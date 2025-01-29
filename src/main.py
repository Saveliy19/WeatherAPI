from fastapi import FastAPI

from API.routes import main_router
from API.dependencies import weather_service

from DAL.database import init_db
import asyncio

import uvicorn

app = FastAPI()
app.include_router(router = main_router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    asyncio.create_task(weather_service.update_all_forecasts())
    
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)