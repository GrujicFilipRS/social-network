from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from utils import NotificationController
from schemas import ExistsGetResponse, DTO, UserListResponse, UserGetResponse
from models import Follow, User

from ..service_models import FollowServiceModel


class FollowServiceSqlal(FollowServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def exists(self, follower_id: UUID, followed_id: UUID) -> ExistsGetResponse:
        exists = self.db_session.query(Follow).filter_by(
            follower_id = follower_id,
            followed_id = followed_id
        ).first() is not None
        
        return ExistsGetResponse.ok(exists)
    
    async def create_follow(self, follower_id: UUID, followed_id: UUID) -> DTO:
        exists = self.db_session.query(Follow).filter_by(
            follower_id = follower_id,
            followed_id = followed_id
        ).first() is not None
        
        if exists:
            return DTO.error('User already follows that user')
        
        users_exist = self.db_session.query(User).filter(id == follower_id or id == followed_id).count() == 2
        if not users_exist:
            return DTO.error('Users do not exist')
        
        follow = Follow(
            follower_id = follower_id,
            followed_id = followed_id,
            followed_datetime = datetime.now(timezone.utc)
        )
        
        self.db_session.add(follow)
        self.db_session.commit()
        
        await NotificationController.create_notification(
            session=self.db_session,
            receiver_id=followed_id,
            sender_id=follower_id,
            object_type='follow',
            object_id=follow.id
        )
        
        return DTO.ok()
    
    async def remove_follow(self, follower_id: UUID, followed_id: UUID) -> DTO:
        follow = self.db_session.query(Follow).filter_by(
            follower_id = follower_id,
            followed_id = followed_id
        ).first()
        
        if not follow:
            return DTO.error('Follow doesn\'t exist')
        
        self.db_session.delete(follow)
        self.db_session.commit()
        
        return DTO.ok()
    
    async def get_user_follows(self, user_id: UUID) -> UserListResponse:
        user = self.db_session.get(User, user_id)
        if not user:
            return UserListResponse.error('User doesn\'t exist')
        
        return UserListResponse.ok([follow.follower for follow in user.follows])

    async def get_user_followers(self, user_id: UUID) -> UserListResponse:
        user = self.db_session.get(User, user_id)
        if not user:
            return UserListResponse.error('User doesn\'t exist')
        
        return UserListResponse.ok([follow.followed for follow in user.followers])
    
    async def get_follower_from_follow(self, follow_id: UUID) -> UserGetResponse:
        follow = self.db_session.get(Follow, follow_id)
        
        if not follow:
            return UserGetResponse.error('Follow not found')
        
        return UserGetResponse.ok(follow.follower)
        
    async def get_followed_from_follow(self, follow_id: UUID) -> UserGetResponse:
        follow = self.db_session.get(Follow, follow_id)
            
        if not follow:
            return UserGetResponse.error('Follow not found')
            
        return UserGetResponse.ok(follow.followed)