from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated

from ..server.db.models.comments import Comment
from api.server.db.models.posts import Post
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

from fastapi import APIRouter, Header

router = APIRouter()


class CommentCreator(BaseModel):
    body: str
    post_id: int
    comment_id: int | None


@router.get('/get_comment/')
def get_comment(comment_id: int) -> JSONResponse:
    try:
        db_sess = create_session()
        
        comment: Comment | None = db_sess.get(Comment, comment_id)

        if not comment:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)
        
        content: dict[str, str | dict] = {
            'message': 'Comment found',
            'comment': comment.to_dict()
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting comment: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.post('/post_comment/')
def post_comment(
    data: CommentCreator,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    try:
        token: str = headers.Authorization
        if not token:
            return JSONResponse(content={'message': 'You are not authorized to post comments'}, status_code=401)
        
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1:
            return JSONResponse(content={'message': 'You are not authorized to post comments'}, status_code=401)

        db_sess = create_session()
        
        new_comment = Comment()
        new_comment.body = data.body
        new_comment.post_id = data.post_id
        new_comment.comment_id = data.comment_id
        new_comment.creator_id = user_id

        db_sess.add(new_comment)
        db_sess.commit()

        content: dict = {
            'message': 'Comment posted',
            'comment': new_comment.to_dict()
        }

        return JSONResponse(content=content, status_code=201)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting comment: {e}'}, status_code=400)

    finally:
        db_sess.close()