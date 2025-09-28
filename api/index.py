from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .server.db import db_session
from .server.db.models.__all_models import *

from .server.conf import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_session.global_init(Config.DBNAME)
    yield

app = FastAPI(lifespan=lifespan)

FRONTEND_URL: str = os.getenv('FRONTEND_URL')

app.add_middleware(
    CORSMiddleware,
    allow_origins = [FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Loading in the endpoints (hopefully)
from .services import (
    user,
    post
)

@app.get('/')
def index():
    return {'message': 'success'}

@app.get('/test')
def test():
    return {'message': 'testpage'}