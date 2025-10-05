from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase

class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    post_id = Column(Integer, nullable=False)
    comment_id = Column(Integer, nullable=True)
    creator_id = Column(Integer, nullable=False)
    commented_at = Column(DateTime, nullable=True)

    post = relationship('Post', foreign_keys=[post_id], back_populates='comments')
    comment = relationship('Comment', foreign_keys=[comment_id])
    creator = relationship('User', foreign_keys=[creator_id], back_populates='comments')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'body': self.body,
            'post': self.post.to_dict(),
            'comment': self.comment.to_dict(),
            'creator': self.creator.to_dict(),
            'commented_at': str(self.commented_at)
        }