from abc import abstractmethod
from uuid import UUID

from schemas import DTO, ExistsGetResponse, UserGetResponse, UserListResponse


class FollowServiceModel:
    @abstractmethod
    async def exists(self, follower_id: UUID, followed_id: UUID) -> ExistsGetResponse: ...
    
    @abstractmethod
    async def create_follow(self, follower_id: UUID, followed_id: UUID) -> DTO: ...
    
    @abstractmethod
    async def remove_follow(self, follower_id: UUID, followed_id: UUID) -> DTO: ...
    
    @abstractmethod
    async def get_user_follows(self, user_id: UUID) -> UserListResponse: ...
    
    @abstractmethod
    async def get_user_followers(self, user_id: UUID) -> UserListResponse: ...
    
    @abstractmethod
    async def get_follower_from_follow(self, follow_id: UUID) -> UserGetResponse: ...
    
    @abstractmethod
    async def get_followed_from_follow(self, follow_id: UUID) -> UserGetResponse: ...