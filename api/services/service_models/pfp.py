from abc import abstractmethod
from typing import BinaryIO
from uuid import UUID

from schemas import DTO


class PfpServiceModel:
    @abstractmethod
    async def create_pfp(self, user_id: UUID, image_stream: BinaryIO) -> DTO: ...