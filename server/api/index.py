from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from server.db import db_session
from server.db.models.__all_models import *

from server.conf import Config

app = FastAPI()

FRONTEND_URL: str = os.getenv('FRONTEND_URL')

app.add_middleware(
    CORSMiddleware,
    allow_origins = [FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading in the endpoints (hopefully)
from server.api.resources import (
    user
)

db_session.global_init(Config.DBNAME)