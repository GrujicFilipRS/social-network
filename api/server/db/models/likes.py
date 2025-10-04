from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase

class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    liked_at = Column(DateTime, nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='likes')
    post = relationship('Post', foreign_keys=[post_id], back_populates='likes')

    def to_dict(self) -> dict:
        content: dict = {
            'id': self.id,
            'post': self.post.to_dict(),
            'user': self.user.to_dict(),
            'liked_at': str(self.liked_at)
        }

        return content