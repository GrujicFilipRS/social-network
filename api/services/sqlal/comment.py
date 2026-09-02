from datetime import datetime, timezone
from uuid import UUID

from models import Comment, Post, User
from schemas import DTO, CommentGetResponse, CommentListResponse, IntegerGetResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..service_models import CommentServiceModel
from .notification import NotificationServiceSqlal


class CommentServiceSqlal(CommentServiceModel):
    def __init__(self, db_sess: Session):
        self.db_session = db_sess
        self.notification_service = NotificationServiceSqlal(db_sess)
    
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
        comment_id: UUID | None
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
            creator_id=user.id,
            comment_id=comment.id if comment else None,
            commented_at=datetime.now(timezone.utc)
        )
        
        self.db_session.add(comment)
        self.db_session.commit()
        
        if post.user_id != user.id:
            await self.notification_service.create_notification(
                receiver_id=post.user_id,
                sender_id=user.id,
                object_type='comment',
                object_id=comment.id
            )
        
        return CommentGetResponse.ok(comment)
    
    async def get_post_num_comments(self, post_id, user_id) -> IntegerGetResponse:
        post = self.db_session.get(Post, post_id)
                
        if not post:
            return IntegerGetResponse.error('Post not found')
                
        if post.status == 'PRIVATE' and (not user_id or post.user_id != user_id):
            return IntegerGetResponse.error('Post not found')
        
        count: int = self.db_session.scalar(
            select(func.count())
            .select_from(Comment)
            .where(Comment.post_id == post_id)
        )
        
        return IntegerGetResponse.ok(count)
    
    async def get_post_comments(self, post_id, user_id) -> CommentListResponse:
        post = self.db_session.get(Post, post_id)
                        
        if not post:
            return CommentListResponse.error('Post not found')
                        
        if post.status == 'PRIVATE' and (not user_id or post.user_id != user_id):
            return CommentListResponse.error('Post not found')
        
        comments: list[Comment] = list(self.db_session.query(Comment).filter(Comment.post_id == post_id))
        
        return CommentListResponse.ok(comments)
    
    async def remove_comment(self, comment_id, user_id) -> DTO:
        comment = self.db_session.get(Comment, comment_id)
        
        if not comment:
            return DTO.error('Comment not found')
        
        if comment.post.status == 'PRIVATE' and (not user_id or comment.post.user_id != user_id):
            return DTO.error('Comment not found')
        
        if comment.creator_id != user_id:
            return DTO.error('Unauthorized')
        
        self.db_session.delete(comment)
        self.db_session.commit()
        
        return DTO.ok()
