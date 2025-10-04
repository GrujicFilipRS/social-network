from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated

from ..server.db.models.likes import Like
from ..server.db.models.users import User
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader
from .literals import PostLiterals

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_like/')
def get_like(
    like_id: int,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    try:
        db_sess = create_session()

        like: Like | None = db_sess.get(Like, like_id)

        if not like:
            return JSONResponse(content={'message': 'Like not found'}, status_code=404)
        
        if like.post.status == PostLiterals.PRIVATE:
            token: str = headers.Authorization
            user_id: int = jwt_tokens.get_user_from_token(token)
            
            if not user_id == like.post.user_id:
                return JSONResponse(content={'message': 'The liked post is private'}, status_code=401)

        content: dict = {
            'message': 'Like successfully found',
            'like': like.to_dict()
        }

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Unexpected error while getting like: {e}'}, status_code=400)
    
    finally:
        db_sess.close()
