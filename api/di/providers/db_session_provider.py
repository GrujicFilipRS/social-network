from collections.abc import Generator

from db import DBSessionManager
from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session


class DBSessionProvider(Provider):
    def __init__(self, db_sess: Session | None = None):
        super().__init__()
        self._db_sess = db_sess

    @provide(scope=Scope.REQUEST)
    def db_sess(self) -> Generator[Session, None, None]:
        with DBSessionManager() as session:
            yield session
            
    @provide(scope=Scope.SESSION)
    def db_sess_session(self) -> Generator[Session, None, None]:
        with DBSessionManager() as session:
            yield session