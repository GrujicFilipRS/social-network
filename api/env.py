# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from pathlib import Path
from dotenv import load_dotenv
from os import getenv, environ

load_dotenv()

REQUIRED_ENV_VARS = (
    'DATABASE_URL',
    'SECRET_KEY',
    'CLOUDINARY_CLOUD_NAME',
    'CLOUDINARY_API_KEY',
    'CLOUDINARY_API_SECRET',
)

raise_exc: bool = False
missing_vars: list[str] = []

for var in REQUIRED_ENV_VARS:
    if var not in environ.keys():
        raise_exc = True
        missing_vars.append(var)
    
if raise_exc:
    raise Exception(f'Missing required environment variables: { ', '.join(missing_vars) }')

class Env:
    def __new__(cls):
        raise TypeError('Env is a static configuration class')
    
    CLOUDINARY_CLOUD_NAME = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = getenv('CLOUDINARY_API_SECRET')
    SECRET_KEY = getenv('SECRET_KEY')
    DATABASE_URL = getenv('DATABASE_URL')
    FRONTEND_URL = getenv('FRONTEND_URL', 'http://localhost:5173')
    JWT_EXPIRATION_HOURS = float(getenv('JWT_EXPIRATION_HOURS', '24'))
    FLASK_ENV = getenv('FLASK_ENV', 'development')
    CLOUDINARY_PFP_FOLDER = getenv('CLOUDINARY_PFP_FOLDER', 'fastapi_uploads_pfp')