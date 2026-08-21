from abc import abstractmethod
from typing import BinaryIO
from uuid import UUID, uuid7


class ImageUploadServiceModel:
    @abstractmethod
    async def init(self) -> None: ...
    
    @abstractmethod
    async def test_connection(self) -> None: ...
    
    @abstractmethod
    async def create_image(self, stream: BinaryIO, filename: str = str(uuid7())) -> tuple[str, str]: ...
    
    @abstractmethod
    async def destroy_image(self, public_id: UUID): ...