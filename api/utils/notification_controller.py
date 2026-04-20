from uuid import UUID

from models import Notification
from sqlalchemy.orm import Session


class NotificationController:
    '''
    Controller class for handling creation of notifications
    and communication with the notification microservice.
    '''
    
    @staticmethod
    def create_notification(
        session: Session,
        receiver_id: UUID,
        sender_id: UUID,
        object_type: str,
        object_id: UUID
    ) -> Notification:
        # Create notification in the database
        notification = Notification(
            receiver_id=receiver_id,
            sender_id=sender_id,
            object_type=object_type,
            object_id=object_id
        )
        session.add(notification)
        session.commit()
        
        # TODO Send notification to notification microservice
        
        return notification