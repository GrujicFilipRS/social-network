from abc import abstractmethod
from uuid import UUID

from schemas import LikeGetResponse, DTO


class LikeServiceModel:
    @abstractmethod
    async def get_like(self, id: UUID, user_id: UUID | None) -> LikeGetResponse: ...
    
    @abstractmethod
    async def like_post(self, post_id: UUID, user_id: UUID | None) -> DTO: ...