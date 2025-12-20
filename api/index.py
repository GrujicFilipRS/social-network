from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
import traceback

from server.db import db_session
from server.db.models.__all_models import *

from server.conf import Config

from router import configure_routing

db_session.global_init(Config.DBNAME)
load_dotenv()

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

configure_routing(app)