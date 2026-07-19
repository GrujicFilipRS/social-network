from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from services.service_models import (
    AuthServiceModel,
    UserServiceModel,
    FollowServiceModel,
    PostServiceModel,
    ImageUploadServiceModel,
    PfpServiceModel,
    LikeServiceModel,
    NotificationModelServiceModel
)
from services.sqlal import (
    AuthServiceJWTSqlal,
    UserServiceSqlal,
    FollowServiceSqlal,
    PostServiceSqlal,
    PfpServiceSqlal,
    LikeServiceSqlal,
    NotificationModelServiceSqlal
)
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
    def pfp_service(self, db_sess: Session, upload_service: ImageUploadServiceModel) -> PfpServiceModel:
        return PfpServiceSqlal(db_sess, upload_service)
    
    @provide(scope=Scope.REQUEST)
    def auth_service(self, db_sess: Session) -> AuthServiceModel:
        return AuthServiceJWTSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def notification_model_service(self, db_sess: Session) -> NotificationModelServiceModel:
        return NotificationModelServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def like_service(self, db_sess: Session) -> LikeServiceModel:
        return LikeServiceSqlal(db_sess)
    
    @provide(scope=Scope.REQUEST)
    def image_service(self) -> ImageUploadServiceModel:
        return ImageServiceCloudinary()
    
    @provide(scope=Scope.APP)
    def image_service_app(self) -> ImageUploadServiceModel:
        return ImageServiceCloudinary()