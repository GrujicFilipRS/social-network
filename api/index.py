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

from .services.user import router as user_router
from .services.post import router as post_router

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(post_router, prefix="/post", tags=["post"])