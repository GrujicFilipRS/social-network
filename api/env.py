import dotenv, os

dotenv.load_dotenv()

def verify_env_vars() -> None:
    REQUIRED_ENV_VARS = (
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET',
        'SECRET_KEY'
    )

    raise_exc: bool = False
    missing_vars: list[str] = []

    for var in REQUIRED_ENV_VARS:
        if var not in os.environ.keys():
            raise_exc = True
            missing_vars.append(var)
    
    if raise_exc:
        raise Exception(f'Missing required environment variables: { ', '.join(missing_vars) }')

verify_env_vars()

def get_local_db_string(db_name: str) -> str:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_dir = os.path.join(base_dir, 'db')

    os.makedirs(db_dir, exist_ok=True)

    return f'sqlite://{os.path.join(db_dir, f"{db_name.strip()}.sqlite")}?check_same_thread=False'

class Env:
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    JWT_EXPIRATION_HOURS = float(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    DATABASE_URL = os.getenv('DATABASE_URL', get_local_db_string('network'))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')