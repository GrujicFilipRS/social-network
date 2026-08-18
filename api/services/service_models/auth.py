from abc import abstractmethod
from uuid import UUID

from models import User


class AuthServiceModel:
    def __init__(self):
        self.auth_token_name = 'auth_token'
    
    @abstractmethod
    def encode_token(self, user_id: UUID | str) -> str: ...
    
    @abstractmethod
    def decode_token(self, token: str | None) -> UUID | None: ...
    
    @abstractmethod
    def get_user_from_token(self, token: str) -> User | None: ...
