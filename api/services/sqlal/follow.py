from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from schemas import ExistsGetResponse, DTO
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
        
        return DTO.ok()