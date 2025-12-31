from sqlalchemy import Column, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase
from uuid import uuid4

class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    post_id = Column(UUID, ForeignKey('posts.id'), nullable=False)
    liked_at = Column(DateTime, nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='likes')
    post = relationship('Post', foreign_keys=[post_id], back_populates='likes')

    def to_dict(self) -> dict:
        content: dict = {
            'id': str(self.id),
            'post': self.post.to_dict(),
            'user': self.user.to_dict(),
            'liked_at': str(self.liked_at)
        }

        return content