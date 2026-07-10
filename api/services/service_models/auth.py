from abc import abstractmethod
from uuid import UUID

from models import User


class AuthServiceModel:
    @abstractmethod
    def encode_token(self, user_id: UUID) -> str: ...
    
    @abstractmethod
    def decode_token(self, token: str) -> UUID | None: ...
    
    @abstractmethod
    def get_user_from_token(self, token: str) -> User | None: ...
