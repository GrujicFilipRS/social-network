from abc import abstractmethod
from uuid import UUID

from schemas import DTO, PostGetResponse, PostListResponse


class PostServiceModel:
    @abstractmethod
    async def get_post(self, id: UUID) -> PostGetResponse: ...
    
    @abstractmethod
    async def remove_post(self, id: UUID) -> DTO: ...
    
    @abstractmethod
    async def get_user_posts(self, id: UUID, filter_private: bool = False) -> PostListResponse: ...