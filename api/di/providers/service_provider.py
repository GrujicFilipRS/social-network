from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from services.service_models import (
    UserServiceModel,
    FollowServiceModel,
    PostServiceModel,
    ImageUploadServiceModel
)
from services.sqlal import UserServiceSqlal, FollowServiceSqlal, PostServiceSqlal
from services.cloudinary import ImageServiceCloudinary


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, db_sess: Session) -> UserServiceModel:
        return UserServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def follow_service(self, db_sess: Session) -> FollowServiceModel:
        return FollowServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def post_service(self, db_sess: Session) -> PostServiceModel:
        return PostServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def image_service(self) -> ImageUploadServiceModel:
        return ImageServiceCloudinary()
    
    @provide(scope=Scope.APP)
    def image_service_app(self) -> ImageUploadServiceModel:
        return ImageServiceCloudinary()