from uuid import UUID

from sqlalchemy.orm import Session

from models import Post, User

from ..service_models import PostServiceModel
from schemas import PostGetResponse, PostListResponse, DTO


class PostServiceSqlal(PostServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_post(self, id: UUID) -> PostGetResponse:
        post = self.db_session.get(Post, id)
        
        if not post:
            return PostGetResponse.error('Post not found')
        
        return PostGetResponse.ok(post)

    async def remove_post(self, id: UUID) -> DTO:
        post = self.db_session.get(Post, id)
        
        if not post:
            return DTO.error('Post not found')
        
        self.db_session.delete(post)
        self.db_session.commit()
        
        return DTO.ok()
    
    async def get_user_posts(self, id: UUID) -> PostListResponse:
        user = self.db_session.get(User, id)
        
        if not user:
            return PostListResponse.error('User not found')
        
        posts = user.posts
        
        return PostListResponse.ok(posts)