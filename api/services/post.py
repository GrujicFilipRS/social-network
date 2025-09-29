from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

from ..server.db.models.posts import Post
from ..server.db.models.users import User
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens

from ..services.literals import PostLiterals

from .authorization import AuthorizationHeader

from fastapi import APIRouter

router = APIRouter()

class PostCreator(BaseModel):
    title: str
    body: str
    status: str


class PostEditor(BaseModel):
    id: int
    title: str
    body: str
    status: str


@router.get('/get_post/')
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
            return JSONResponse(content={'message': 'You are not authorized to view this post'}, status_code=401)
        
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1 or user_id != post.user_id:
            return JSONResponse(content={'message': 'You are not authorized to view this post'}, status_code=401)

        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting post: {e}'}, status_code=400)

    finally:
        db_sess.close()


@router.post('/create_post/')
def create_post(
    data: PostCreator,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    
    token: str = headers.Authorization

    try:
        if not token:
            return JSONResponse(content={'message': 'You are not authorized to create posts'}, status_code=401)
        
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1:
            return JSONResponse(content={'message': 'You are not authorized to create posts'}, status_code=401)
        
        db_sess = create_session()

        post = Post()
        post.set_title(data.title)
        post.set_body(data.body)
        post.set_status(data.status)
        post.user_id = user_id
        post.created_at = datetime.now()

        db_sess.add(post)
        db_sess.commit()

        content: dict = {
            'message': 'Successfully created post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=201)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while creating post: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.put('/edit_post/')
def edit_post(
    data: PostEditor,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    
    token: str = headers.Authorization

    try:
        if not token:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)

        db_sess = create_session()
        post = db_sess.get(Post, data.id)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        post.set_title(data.title)
        post.set_body(data.body)
        post.set_status(data.status)

        db_sess.add(post)
        db_sess.commit()

        content: dict = {
            'message': 'Successfully edited post',
            'post': post.to_dict()
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while editing post: {e}'}, status_code=400)

    finally:
        db_sess.close()


@router.delete('/delete_post/')
def delete_post(
    post_id: int | None,
    headers: Annotated[AuthorizationHeader, Header()]
) -> JSONResponse:
    
    token: str = headers.Authorization

    try:
        if not token:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
                
        user_id: int = jwt_tokens.get_user_from_token(token)
        if user_id == -1:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        db_sess = create_session()

        post = db_sess.get(Post, post_id)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to edit this post'}, status_code=401)
        
        db_sess.delete(post)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successully deleted post'}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while deleting post: {e}'}, status_code=400)
    
    finally:
        db_sess.close()