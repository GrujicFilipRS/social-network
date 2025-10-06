from fastapi.responses import JSONResponse

from ..server.db.models.comments import Comment
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_comment/')
def get_comment(comment_id: int) -> JSONResponse:
    try:
        db_sess = create_session()
        
        comment: Comment | None = db_sess.get(Comment, comment_id)

        if not comment:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)
        
        content: dict = {
            'message': 'Comment found',
            'comment': comment.to_dict()
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting comment: {e}'}, status_code=400)
    
    finally:
        db_sess.cloose()