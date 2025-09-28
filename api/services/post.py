from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

from ..server.db.models.posts import Post
from ..server.db.models.users import User
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens

from ..index import app

from ..services.literals import PostLiterals

class AuthorizationHeader(BaseModel):
    Authorization: str


@app.get('/post/get_post/')
async def get_post(
    post_id: int | None,
    headers: Annotated[AuthorizationHeader, Header()],
    req_creation_date: bool=False,
    req_user: bool=False
) -> JSONResponse:
    
    token: str = headers.Authorization

    db_sess = create_session()

    if not post_id:
        return JSONResponse(content={'message': '`post_id` parameter is necessary'}, status_code=400)
    
    try:
        post = db_sess.get(Post, post_id)
        
        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        post_info: dict = post.to_dict(req_creation_date=req_creation_date)

        content: dict = {
            'message': 'Post found',
            'post': post_info
        }

        if req_user:
            content['user'] = post.user.to_dict(req_name=True)
        else:
            content['user'] = post.user.username

        if post.status == PostLiterals.PUBLIC:
            return JSONResponse(content=content, status_code=200)
        
        if not token:
            return JSONResponse(content={'message': 'You are not authorized to view this post'}, status_code=403)
        
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1 or user_id != post.user_id:
            return JSONResponse(content={'message': 'You are not authorized to view this post'}, status_code=403)

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting post: {e}'}, status_code=500)

    finally:
        db_sess.close()