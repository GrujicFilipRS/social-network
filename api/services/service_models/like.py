from abc import abstractmethod
from uuid import UUID

from schemas import DTO, IntegerGetResponse, LikeGetResponse

from .notification import NotificationServiceModel


class LikeServiceModel:
    @abstractmethod
    async def get_like(self, id: UUID, user_id: UUID | None) -> LikeGetResponse: ...
    
    @abstractmethod
    async def like_post(
        self,
        post_id: UUID,
        user_id: UUID,
        notification_service: NotificationServiceModel
    ) -> DTO: ...
    
    @abstractmethod
    async def unlike_post(self, post_id: UUID, user_id: UUID) -> DTO: ...
    
    @abstractmethod
    async def get_post_num_likes(self, post_id: UUID, user_id: UUID | None) -> IntegerGetResponse: ...