from abc import abstractmethod
from uuid import UUID

from schemas import PhotoListResponse


class PhotoServiceModel:
    @abstractmethod
    async def get_post_photos(self, post_id: UUID, user_id: UUID) -> PhotoListResponse: ...