from abc import abstractmethod
from uuid import UUID

from schemas import NotificationGetResponse

from .notification_model import NotificationModelServiceModel


class NotificationServiceModel:
    @abstractmethod
    async def create_notification(
        self,
        notification_model_service: NotificationModelServiceModel,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> NotificationGetResponse:
        ...