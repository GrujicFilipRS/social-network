from datetime import datetime, timezone
from uuid import UUID

from models import Comment, Post, User
from schemas import CommentGetResponse
from sqlalchemy.orm import Session

from ..service_models import CommentServiceModel


class CommentServiceSqlal(CommentServiceModel):
    def __init__(self, db_sess: Session):
        self.db_session = db_sess
    
    async def get_comment(self, comment_id, user_id) -> CommentGetResponse:
        comment = self.db_session.get(Comment, comment_id)
        
        if not comment:
            return CommentGetResponse.error('Comment not found')
        
        if comment.post.status == 'PRIVATE' and comment.post.user_id != user_id:
            return CommentGetResponse.error('Comment not found')
        
        return CommentGetResponse.ok(comment)
    
    async def post_comment(
        self,
        body: str,
        post_id: UUID,
        user_id: UUID,
        comment_id: UUID | None = None
    ) -> CommentGetResponse:
        user = self.db_session.get(User, user_id)
        if not user:
            return CommentGetResponse.error('Unauthorized')
        
        post = self.db_session.get(Post, post_id)
        if not post:
            return CommentGetResponse.error('Post not found')
        
        if post.status == 'PRIVATE' and post.user_id != user_id:
            return CommentGetResponse.error('Post not found')
        
        comment = None
        if comment_id:
            comment = self.db_session.get(Comment, comment_id)
            if not comment:
                return CommentGetResponse.error('Comment not found')
        
        comment = Comment(
            body=body,
            post_id=post.id,
            user_id=user.id,
            comment_id=comment.id if comment else None,
            commented_at=datetime.now(timezone.utc)
        )
        self.db_session.add(comment)
        self.db_session.commit()
        
        return CommentGetResponse.ok(comment)