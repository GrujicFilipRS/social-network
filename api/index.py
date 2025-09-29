from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.responses import JSONResponse
import traceback

from .server.db import db_session
from .server.db.models.__all_models import *

from .server.conf import Config

db_session.global_init(Config.DBNAME)

app = FastAPI()

FRONTEND_URL: str = os.getenv('FRONTEND_URL', '*')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
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


from .services.user import router as user_router
from .services.post import router as post_router
from .services.follow import router as follow_router

app.include_router(user_router, prefix='/user', tags=['user'])
app.include_router(post_router, prefix='/post', tags=['post'])
app.include_router(follow_router, prefix='/follow', tags=['follow'])