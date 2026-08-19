from abc import abstractmethod
from uuid import UUID

from schemas import CommentGetResponse


class CommentServiceModel:
    @abstractmethod
    async def get_comment(self, comment_id: UUID, user_id: UUID) -> CommentGetResponse: ...
    
    @abstractmethod
    async def post_comment(
        self,
        body: str,
        post_id: UUID,
        user_id: UUID,
        comment_id: UUID | None = None
    ) -> CommentGetResponse: ...