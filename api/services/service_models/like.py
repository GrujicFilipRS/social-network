from abc import abstractmethod
from uuid import UUID

from schemas import DTO, LikeGetResponse
from services.service_models import (
    NotificationModelServiceModel,
    NotificationServiceModel,
)


class LikeServiceModel:
    @abstractmethod
    async def get_like(self, id: UUID, user_id: UUID | None) -> LikeGetResponse: ...
    
    @abstractmethod
    async def like_post(
        self,
        post_id: UUID,
        user_id: UUID,
        notification_service: NotificationServiceModel,
        notification_model_service: NotificationModelServiceModel
    ) -> DTO: ...
    
    @abstractmethod
    async def unlike_post(self, post_id: UUID, user_id: UUID) -> DTO: ...