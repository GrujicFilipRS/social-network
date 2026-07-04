from dishka import Provider, Scope, provide

from ...services.service_models import UserServiceModel
from ...services.sqlal import UserServiceSqlal


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def user_service(self) -> UserServiceModel:
        return UserServiceSqlal()