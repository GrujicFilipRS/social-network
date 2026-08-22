from models import Post
from schemas import PhotoListResponse
from services.service_models import PhotoServiceModel
from sqlalchemy.orm import Session


class PhotoServiceSqlal(PhotoServiceModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def get_post_photos(self, post_id, user_id) -> PhotoListResponse:
        post = self.db_session.get(Post, post_id)
        
        if not post:
            return PhotoListResponse.error('Post not found')
        
        if post.user_id != user_id and post.status == 'PRIVATE':
            return PhotoListResponse.error('Post not found')
        
        return PhotoListResponse.ok(post.photos)