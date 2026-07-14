from abc import abstractmethod
from uuid import UUID

from schemas import NotificationListResponse, DTO


class NotificationModelServiceModel:
    @abstractmethod
    async def get_unread_notifications(self, user_id: UUID) -> NotificationListResponse: ...
    
    @abstractmethod
    async def read_notification(self, notification_id: UUID, user_id: UUID) -> DTO: ...