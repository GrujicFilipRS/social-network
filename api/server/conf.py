import os, random

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', f'social-{random.randint(0, 1000000)}')
    JWT_EXPIRATION_HOURS: float = float(os.getenv('JWT_EXPIRATION_HOURS', '24'))

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DBNAME: str = r'db/network.sqlite'