from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from services.service_models import UserServiceModel, FollowServiceModel
from services.sqlal import UserServiceSqlal, FollowServiceSqlal


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, db_sess: Session) -> UserServiceModel:
        return UserServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def follow_service(self, db_sess: Session) -> FollowServiceModel:
        return FollowServiceSqlal(db_sess)