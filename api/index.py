from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
import traceback

from env import Env
from db import db_session
from models.__all_models import *

from router import configure_routing
from utils.image_controller import ImageController

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
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=400,
        content={'message': str(exc)}
    )

configure_routing(app)

ImageController.setup_connection()
ImageController.test_connection()