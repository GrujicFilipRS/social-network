from abc import abstractmethod
from uuid import UUID

from schemas import DTO, NotificationGetResponse, NotificationListResponse


class NotificationModelServiceModel:
    @abstractmethod
    async def get_unread_notifications(self, user_id: UUID) -> NotificationListResponse: ...
    
    @abstractmethod
    async def read_notification(self, notification_id: UUID, user_id: UUID) -> DTO: ...
    
    @abstractmethod
    async def create_notification(
        self,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> NotificationGetResponse: ...