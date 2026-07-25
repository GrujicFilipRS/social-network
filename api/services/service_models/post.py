from abc import abstractmethod
from io import BytesIO
from uuid import UUID

from schemas import DTO, PostGetResponse, PostListResponse


class PostServiceModel:
    @abstractmethod
    async def get_post(self, post_id: UUID, user_id: UUID | None) -> PostGetResponse: ...
    
    @abstractmethod
    async def remove_post(self, id: UUID) -> DTO: ...
    
    @abstractmethod
    async def get_user_posts(self, id: UUID, filter_private: bool = False) -> PostListResponse: ...
    
    @abstractmethod
    async def create_post(
        self,
        user_id: UUID,
        title: str,
        body: str | None,
        status: str,
        image_streams: list[BytesIO]
    ) -> PostGetResponse: ...
    
    @abstractmethod
    async def edit_post(
        self,
        post_id: UUID,
        user_id: UUID,
        title: str,
        body: str | None,
        status: str,
    ) -> DTO: ...
    
    @abstractmethod
    async def delete_post(self, post_id: UUID, user_id: UUID) -> DTO: ...