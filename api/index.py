from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

from server.db import db_session
from server.db.models.__all_models import *

from server.conf import Config

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
from services import (
    user,
    post
)

@app.get('/')
def index():
    return {'message': 'success'}

# For vercel
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host=Config.HOST, port=Config.PORT, reload=True)