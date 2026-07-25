from env import Env
from sqlalchemy import create_engine, orm

SqlAlchemyBase = orm.declarative_base()
__factory: orm.sessionmaker[orm.Session] | None = None

def global_init():
    global __factory

    if __factory:
        return

    connection_string = Env.DATABASE_URL

    print('Connecting to remote DB')

    engine = create_engine(
        connection_string,
        echo=False,
        future=True,
        pool_pre_ping=True
    )
    
    __factory = orm.sessionmaker(bind=engine, autoflush=False, autocommit=False)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    if not __factory:
        global_init()
    return __factory()


class DBSessionManager:
    def __init__(self):
        self.db_sess = create_session()

    def __enter__(self):
        return self.db_sess

    def __exit__(self, exc_type, exc_val, _):
        self.db_sess.close()
        if exc_type:
            print(f'Exception in DB session: {exc_type}, {exc_val}')