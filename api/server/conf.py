class Config:
    SECRET_KEY: str = 'network'
    JWT_EXPIRATION_HOURS: float = 24

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DBNAME: str = r'db/network.sqlite'
    HOST: str = "localhost"
    PORT: int = 8000