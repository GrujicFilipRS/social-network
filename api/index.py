import asyncio
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
import traceback

from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from di.providers import DBSessionProvider, ServiceProvider
from services.service_models import ImageUploadServiceModel
from schemas import DTO
from env import Env
from db import db_session

from utils import WorkerShareController, ConnectionController
from routers import router

db_session.global_init()

@asynccontextmanager
async def lifespan(app: FastAPI):
    image_service = await container.get(ImageUploadServiceModel)

    await image_service.init()
    await image_service.test_connection()

    WorkerShareController.init()

    redis_task = asyncio.create_task(ConnectionController.redis_listener())

    yield

    redis_task.cancel()
    try:
        await redis_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Env.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content=DTO.error('Invalid data').__dict__,
        status_code=400
    )

@app.exception_handler(Exception)
async def global_exception_handler(req: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        content=DTO.error('Internal server error').__dict__,
        status_code=500
    )
    

container = make_async_container(
    DBSessionProvider(),
    ServiceProvider()
)

setup_dishka(container=container, app=app)

app.include_router(router)
