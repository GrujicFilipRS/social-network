import string
from typing import Any
import unicodedata
from sqlalchemy import Column, UUID, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.db_session import SqlAlchemyBase
from uuid import uuid4

class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = Column(UUID, primary_key=True, default=uuid4)
    body = Column(Text, nullable=False)
    post_id = Column(UUID, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    comment_id = Column(UUID, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    commented_at = Column(DateTime, nullable=True)

    post = relationship('Post', foreign_keys=[post_id], back_populates='comments')
    comment = relationship('Comment', foreign_keys=[comment_id])
    creator = relationship('User', foreign_keys=[creator_id], back_populates='comments')

    def to_dict(self) -> dict[str, Any]:
        content: dict[str, Any] = {
            'id': str(self.id),
            'body': self.body,
            'post_id': str(self.post_id),
            'comment_id': str(self.comment_id) if self.comment_id else None,
            'creator': self.creator.to_dict(),
            'commented_at': str(self.commented_at)
        }
        
        return content
    
    @staticmethod
    def validate_body(data: Any) -> bool:
        body = data.get('body')
        
        if not body or not isinstance(body, str):
            return False

        body = body.strip()

        MIN_BODY_LENGTH = 1
        MAX_BODY_LENGTH = 80

        if len(body) < MIN_BODY_LENGTH or len(body) > MAX_BODY_LENGTH:
            return False

        MAX_BODY_LINES = 3
        if body.count('\n') > MAX_BODY_LINES:
            return False

        if not all(c in string.printable for c in body):
            return False

        DANGEROUS_SUBSTRINGS = (
            '<script',
            '</script',
            'javascript:',
            'onerror=',
            'onload=',
            '<iframe',
            '</iframe',
        )

        lower_body = body.lower()
        if any(x in lower_body for x in DANGEROUS_SUBSTRINGS):
            return False

        if any(
            unicodedata.category(c) in ('Cc', 'Cf') and c not in '\n\r\t'
            for c in body
        ):
            return False
        
        if not body.replace('\n', '').strip():
            return False
        
        return True
    
    @staticmethod
    def validate_creation(data: dict[str, Any]) -> bool:
        post_id = data.get('post_id')
        comment_id = data.get('comment_id')
        
        if not Comment.validate_body(data):
            return False
        
        if not post_id or not isinstance(post_id, str):
            return False
        
        if comment_id and not isinstance(comment_id, str):
            return False
        
        try:
            UUID(post_id)
            UUID(comment_id) if comment_id else None
        except ValueError:
            return False
        
        return True