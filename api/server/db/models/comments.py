from sqlalchemy import Column, UUID, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase
from uuid import uuid4

class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = Column(UUID, primary_key=True, default=uuid4)
    body = Column(Text, nullable=False)
    post_id = Column(UUID, ForeignKey('posts.id'), nullable=False)
    comment_id = Column(UUID, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    commented_at = Column(DateTime, nullable=True)

    post = relationship('Post', foreign_keys=[post_id], back_populates='comments')
    comment = relationship('Comment', foreign_keys=[comment_id])
    creator = relationship('User', foreign_keys=[creator_id], back_populates='comments')

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'body': self.body,
            'post': self.post.to_dict(),
            'comment': self.comment.to_dict(),
            'creator': self.creator.to_dict(),
            'commented_at': str(self.commented_at)
        }