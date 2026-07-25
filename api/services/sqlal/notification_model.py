from models import Notification, User
from schemas import DTO, NotificationListResponse
from services.service_models import NotificationModelServiceModel
from sqlalchemy.orm import Session


class NotificationModelServiceSqlal(NotificationModelServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_unread_notifications(self, user_id):
        user = self.db_session.get(User, user_id)
        
        if not user:
            return NotificationListResponse.error('Unauthorized')
        
        notifications = self.db_session.query(Notification)\
            .filter_by(seen=False)\
            .filter(Notification.receiver == user).limit(10).all()
        
        return NotificationListResponse.ok(notifications)
    
    async def read_notification(self, notification_id, user_id):
        user = self.db_session.get(User, user_id)
        
        if not user:
            return DTO.error('Unauthorized')
        
        notification = self.db_session.get(Notification, notification_id)
        
        if not notification:
            return DTO.error('Notification doesn\'t exist')
        
        if notification.receiver != user:
            return DTO.error('Unauthorized')
        
        if notification.seen:
            return DTO.error('Notification already seen')
        
        notification.seen = True
        self.db_session.add(notification)
        self.db_session.commit()
        
        return DTO.ok()