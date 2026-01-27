from sqlalchemy import create_engine
import sqlalchemy.orm as orm
import os

SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init(db_file: str = None):
    """
    Initialize the database connection.

    - If DATABASE_URL env var exists -> use that (Postgres/MySQL/etc.)
    - Else -> fallback to local SQLite with db_file
    """
    global __factory

    if __factory:
        return

    connection_string = os.getenv("DATABASE_URL")

    if connection_string:
        print(f"Connecting to remote DB at {connection_string}")
        engine = create_engine(connection_string, echo=False, future=True)
    else:
        if not db_file or not db_file.strip():
            raise Exception("Database file isn't specified and no DATABASE_URL found!")

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        db_path = os.path.abspath(os.path.join(base_dir, db_file.strip()))

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection_string = f"sqlite:///{db_path}?check_same_thread=False"
        print(f"Connecting to SQLite DB at {connection_string}")
        engine = create_engine(connection_string, echo=False, future=True)

    __factory = orm.sessionmaker(bind=engine, autoflush=False, autocommit=False)

    from models import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    if not __factory:
        raise Exception("Database session not initialized. Call global_init first.")
    return __factory()


class DBSessionManager:
    def __init__(self):
        self.db_sess = create_session()

    def __enter__(self):
        return self.db_sess

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_sess.close()
        if exc_type:
            print(f"Exception in DB session: {exc_type}, {exc_val}")