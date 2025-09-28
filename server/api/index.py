from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
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

@app.get('/api/')
def index():
    return {'message': 'success'}

db_session.global_init(Config.DBNAME)

handler = Mangum(app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.api.index:app", host="127.0.0.1", port=8000, reload=True)