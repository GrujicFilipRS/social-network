from __future__ import annotations

from uuid import UUID

from models import Photo
from pydantic import BaseModel

from ..post.post_dto import PostDTO


class PhotoDTO(BaseModel):
    id: UUID
    image_src: str
    image_id: str
    post_position: int
    post: PostDTO | None
    
    @staticmethod
    def to_dto(photo: Photo | PhotoDTO, req_post: bool = False) -> PhotoDTO:
        if isinstance(photo, PhotoDTO):
            return photo
        
        return PhotoDTO(
            id = photo.id,
            image_src = photo.image_src,
            image_id = photo.image_id,
            post_position = photo.post_position,
            post = (PostDTO.to_dto(photo.post) if req_post else None)
        )