from __future__ import annotations

from models import Photo

from ..shared.dto import DTO
from .photo_dto import PhotoDTO


class PhotoListResponse(DTO):
    photos: list[PhotoDTO]
    
    @staticmethod
    def ok(photos: list[Photo] | list[PhotoDTO], message: str | None = None) -> PhotoListResponse:
        photos_dto = [PhotoDTO.to_dto(photo) for photo in photos]
        
        return PhotoListResponse(
            success = True,
            message = message,
            photos = photos_dto
        )
    
    @staticmethod
    def error(message: str) -> PhotoListResponse:
        return PhotoListResponse(
            success = False,
            message = message,
            photos = []
        )