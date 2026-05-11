from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import Session, relationship
from db import SqlAlchemyBase
from models import Like, Comment, Post, Follow


class Notification(SqlAlchemyBase):
    __tablename__ = 'notifications'
    
    id = Column(UUID, primary_key=True, default=uuid4)
    receiver_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    sender_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    object_type = Column(Text, nullable=False)
    object_id = Column(UUID, nullable=False)
    received_at = Column(DateTime, nullable=True)
    seen = Column(Boolean, default=False)
    
    receiver = relationship('User', foreign_keys=[receiver_id])
    sender = relationship('User', foreign_keys=[sender_id])

    def get_object(self, session: Session) -> Like | Comment | Post | Follow | None:
        if self.object_type == 'like':
            return session.get(Like, self.object_id)
        
        elif self.object_type == 'comment':
            return session.get(Comment, self.object_id)
        
        elif self.object_type == 'post':
            return session.get(Post, self.object_id)
        
        elif self.object_type == 'follow':
            return session.get(Follow, self.object_id)
        
        return None