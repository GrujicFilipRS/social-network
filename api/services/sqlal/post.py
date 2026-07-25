from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from models import Photo, Post, User
from schemas import DTO, PostGetResponse, PostListResponse
from services.service_models import ImageUploadServiceModel
from utils import PhotoVerificationMethods

from ..service_models import PostServiceModel


class PostServiceSqlal(PostServiceModel):
    def __init__(
        self,
        db_session: Session,
        upload_service: ImageUploadServiceModel
    ):
        self.db_session = db_session
        self.upload_service = upload_service
    
    async def get_post(self, post_id: UUID, user_id: UUID | None) -> PostGetResponse:
        post = self.db_session.get(Post, post_id)
        
        if not post:
            return PostGetResponse.error('Post not found')
        
        if post.status == 'PRIVATE' and post.user_id != user_id:
            return PostGetResponse.error('Post not found')
        
        return PostGetResponse.ok(post)

    async def remove_post(self, id: UUID) -> DTO:
        post = self.db_session.get(Post, id)
        
        if not post:
            return DTO.error('Post not found')
        
        self.db_session.delete(post)
        self.db_session.commit()
        
        return DTO.ok()
    
    async def get_user_posts(self, id: UUID, filter_private: bool = False) -> PostListResponse:
        user = self.db_session.get(User, id)
        
        if not user:
            return PostListResponse.error('User not found')
        
        posts = self.db_session.query(Post).filter_by(user_id=id)
        
        if filter_private:
            posts = posts.filter(Post.status != 'PRIVATE')
        
        return PostListResponse.ok(list(posts))
    
    async def create_post(self, user_id, title, body, status, image_streams) -> PostGetResponse:
        user = self.db_session.get(User, user_id)
                
        if not user:
            return PostListResponse.error('User not found')
        
        post = Post(
            title = title,
            body = body,
            status = status,
            created_at = datetime.now(timezone.utc),
            user_id=user_id,
        )
        
        self.db_session.add(post)
        self.db_session.flush()
        
        for i, stream in enumerate(image_streams):
            if not PhotoVerificationMethods.verify_photo(stream):
                self.db_session.rollback()
                return PostGetResponse.error('Invalid photo format')
            
            image_src, public_id = await self.upload_service.create_image(stream)
            
            photo = Photo(
                post_id = post.id,
                post_position = i + 1,
                image_src = image_src,
                image_id = public_id
            )
            
            self.db_session.add(photo)
            self.db_session.flush()
        
        self.db_session.commit()
        return PostGetResponse.ok(post)

    async def edit_post(self, post_id, user_id, title, body, status) -> DTO:
        user = self.db_session.get(User, user_id)
                        
        if not user:
            return DTO.error('User not found')
        
        post = self.db_session.get(Post, post_id)
        
        if not post:
            return DTO.error('Post not found')
        
        if post.user != user:
            return DTO.error('Unauthorized')
        
        post.title = title
        post.body = body
        post.status = status
        
        self.db_session.add(post)
        self.db_session.commit()
        
        return DTO.ok()