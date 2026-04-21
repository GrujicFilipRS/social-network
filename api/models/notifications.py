from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, Text
from sqlalchemy.orm import Session
from db import SqlAlchemyBase
from models import Like, Comment, Post, Follow


class Notification(SqlAlchemyBase):
    __tablename__ = 'notifications'
    
    id = Column(UUID, primary_key=True, default=uuid4)
    receiver_id = Column(UUID, nullable=False)
    sender_id = Column(UUID, nullable=False)
    object_type = Column(Text, nullable=False)
    object_id = Column(UUID, nullable=False)
    receiver_at = Column(DateTime, nullable=True)

    def get_object(self, session: Session):
        if self.object_type == 'like':
            return session.get(Like, self.object_id)
        
        elif self.object_type == 'comment':
            return session.get(Comment, self.object_id)
        
        elif self.object_type == 'post':
            return session.get(Post, self.object_id)
        
        elif self.object_type == 'follow':
            return session.get(Follow, self.object_id)
        
        return None