from models import Comment
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