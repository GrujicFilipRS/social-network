from abc import abstractmethod
from uuid import UUID

from schemas import NotificationGetResponse


class NotificationServiceModel:
    @abstractmethod
    async def create_notification(
        self,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> NotificationGetResponse:
        ...