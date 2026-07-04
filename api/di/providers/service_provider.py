from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from services.service_models import UserServiceModel
from services.sqlal import UserServiceSqlal


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, db_sess: Session) -> UserServiceModel:
        return UserServiceSqlal(db_sess)