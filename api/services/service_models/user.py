from abc import abstractmethod
from uuid import UUID

from schemas import DTO, UserGetResponse


class UserServiceModel:
    @abstractmethod
    async def get_user(self, id: UUID) -> UserGetResponse: ...
    
    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserGetResponse: ...
    
    @abstractmethod
    async def register(self, username: str, password: str, name: str | None) -> UserGetResponse: ...
    
    @abstractmethod
    async def log_in(self, username: str, password: str) -> UserGetResponse: ...
    
    @abstractmethod
    async def set_name(self, id: UUID, name: str) -> DTO: ...
    
    @abstractmethod
    async def change_username(self, id: UUID, username: str) -> DTO: ...
    
    @abstractmethod
    async def change_password(self, id: UUID, old_password: str, new_password: str) -> DTO: ...