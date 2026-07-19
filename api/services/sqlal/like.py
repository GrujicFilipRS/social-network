from sqlalchemy.orm import Session

from models import Like
from ..service_models import LikeServiceModel
from schemas import LikeGetResponse


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