from datetime import datetime, timezone

from models import Like, Post, User
from schemas import DTO, LikeGetResponse
from sqlalchemy.orm import Session
from utils import NotificationController

from ..service_models import LikeServiceModel


class LikeServiceSqlal(LikeServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_like(self, id, user_id) -> LikeGetResponse:
        like = self.db_session.get(Like, id)
        
        if not like:
            return LikeGetResponse.error('No like found')
        
        if like.post.status == 'PRIVATE' and like.user_id != user_id:
            return LikeGetResponse.error('No like found')
        
        return LikeGetResponse.ok(like)
    
    async def like_post(self, post_id, user_id) -> DTO:
        if self.db_session.get(User, user_id).first() is None:
            return DTO.error('Unauthorized')
        
        post = self.db_session.get(Post, post_id)
        
        if not post:
            return DTO.error('Post doesn\'t exist')
        
        if post.status == 'PRIVATE' and post.user_id != user_id:
            return DTO.error('Post doesn\'t exist')
        
        like_exists = self.db_session.query(Like)\
            .filter_by(user_id = user_id, post_id = post_id).first() is not None
        
        if like_exists:
            return DTO.error('Post already liked')
        
        like = Like(
            user_id = user_id,
            post_id = post_id,
            liked_at = datetime.now(timezone.utc)
        )
        
        self.db_session.add(like)
        self.db_session.commit()
        
        if post.user_id != user_id:
            await NotificationController.create_notification(
                self.db_session,
                post.user_id,
                user_id,
                'like',
                like.id
            )
        
        return DTO.ok()
    
    async def unlike_post(self, post_id, user_id):
        if self.db_session.get(User, user_id).first() is None:
            return DTO.error('Unauthorized')
        
        post = self.db_session.get(Post, post_id)
        
        if not post:
            return DTO.error('Post doesn\'t exist')
        
        if post.status == 'PRIVATE' and post.user_id != user_id:
            return DTO.error('Post doesn\'t exist')
        
        like = self.db_session.query(Like)\
            .filter_by(user_id = user_id, post_id = post_id).first()
            
        if not like:
            return DTO.error('Post not liked')
        
        self.db_session.delete(like)
        self.db_session.commit()
        
        return DTO.ok()