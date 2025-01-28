from fastapi import FastAPI

from API.routes import main_router

from DAL.database import init_db
import asyncio

import uvicorn

app = FastAPI()
app.include_router(router = main_router)

async def startup():
    await init_db()

if __name__ == '__main__':
    asyncio.run(startup())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)