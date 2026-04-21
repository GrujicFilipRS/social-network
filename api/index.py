from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
import traceback

from env import Env
from db import db_session

from utils import ImageController
from services import router

db_session.global_init()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Env.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(Exception)
async def global_exception_handler(req: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={'message': 'Internal server error'}
    )

app.include_router(router)

ImageController.setup_connection()
ImageController.test_connection()