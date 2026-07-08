from abc import abstractmethod
from io import BytesIO
from uuid import UUID

from schemas import DTO


class PfpServiceModel:
    @abstractmethod
    async def create_pfp(self, user_id: UUID, image_stream: BytesIO) -> DTO: ...