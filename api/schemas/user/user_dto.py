from __future__ import annotations

from pydantic import BaseModel

from models import User

class UserDTO(BaseModel):
    id: str
    username: str
    name: str | None
    pfp_src: str | None
    
    @staticmethod
    def to_dto(user: User | UserDTO) -> UserDTO:
        if isinstance(user, UserDTO):
            return user
        
        return UserDTO(
            id = str(user.id),
            username = user.username,
            name = user.name,
            pfp_src = user.pfp.image_src if user.pfp else None
        )