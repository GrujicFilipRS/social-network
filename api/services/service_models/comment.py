from abc import abstractmethod
from uuid import UUID

from dishka import FromDishka
from schemas import CommentGetResponse, CommentListResponse, IntegerGetResponse

from .notification import NotificationServiceModel


class CommentServiceModel:
    @abstractmethod
    async def get_comment(self, comment_id: UUID, user_id: UUID) -> CommentGetResponse: ...
    
    @abstractmethod
    async def post_comment(
        self,
        body: str,
        post_id: UUID,
        user_id: UUID,
        comment_id: UUID | None,
        notification_service: FromDishka[NotificationServiceModel],
    ) -> CommentGetResponse: ...
    
    @abstractmethod
    async def get_post_num_comments(self, post_id: UUID, user_id: UUID | None) -> IntegerGetResponse: ...
    
    @abstractmethod
    async def get_post_comments(self, post_id: UUID, user_id: UUID | None) -> CommentListResponse: ...