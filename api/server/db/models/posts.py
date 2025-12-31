from sqlalchemy import Column, ForeignKey, UUID, String, DateTime, Text
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase
from uuid import uuid4

class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    body = Column(Text)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')
    comments = relationship('Comment', back_populates='post')
    photos = relationship('Photo', back_populates='post')

    def to_dict(self, req_creation_date=False) -> dict:
        output: dict = {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'status': self.status,
            'user_id': str(self.user_id),
            'photos': [ photo.to_dict() for photo in self.photos ]
        }

        if req_creation_date:
            output['created_at'] = str(self.created_at)
        
        return output

    def set_title(self, title: str) -> None:
        self.title = title
    
    def set_body(self, body: str) -> None:
        self.body = body
    
    def set_status(self, status: str) -> None:
        self.status = status