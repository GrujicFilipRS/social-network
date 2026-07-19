from abc import abstractmethod
from uuid import UUID

from schemas import LikeGetResponse


class LikeServiceModel:
    @abstractmethod
    async def get_like(self, id: UUID, user_id: UUID | None) -> LikeGetResponse: ...