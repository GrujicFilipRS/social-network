from sqlalchemy import create_engine
import sqlalchemy.orm as orm

from env import Env

SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init():
    global __factory

    if __factory:
        return

    connection_string = Env.DATABASE_URL

    print(f"Connecting to remote DB at {connection_string}")
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