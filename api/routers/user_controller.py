from uuid import UUID
from dishka.integrations.fastapi import FromDishka, inject
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Any

from schemas import UserGetResponse
from services.service_models import UserServiceModel
from models import Like, User, UserOptions, Follow, Post
from db import DBSessionManager

from utils import JWT

from fastapi import APIRouter

router = APIRouter()


@router.get(
    '/get_user/',
    response_model=UserGetResponse
)
@inject
async def get_user(
    user_id: UUID,
    user_service: FromDishka[UserServiceModel]
) -> JSONResponse:
    response = await user_service.get_user(user_id)
    
    if not response.success:
        raise HTTPException(status_code=404, detail=response.message)

    return response


@router.get('/get_current_user/')
@JWT.require_auth
def get_current_user(
    request: Request,
    user_id: UUID | None = None,
) -> JSONResponse:
    assert user_id is not None

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.get(User, user_id)
        if not user:
            return JSONResponse(content={'message': 'Invalid token'}, status_code=401)

        content: dict = {
            'message': 'Successful verification',
            'user': user.to_dict()
        }

        return JSONResponse(content=content, status_code=200)


class RegistrationData(BaseModel):
    username: str
    password: str
    name: str | None

@router.post('/register/')
async def register(data: RegistrationData) -> JSONResponse:
    username = data.username
    password = data.password
    name = data.name

    if not username or not password:
        return JSONResponse(content={'message': 'Username and password required'}, status_code=400)
    
    username = username.strip()
    password = password.strip()
    if name is not None:
        name = name.strip()

    if (not User.validate_username(username) or
        not User.validate_password(password) or
        not User.validate_name(name)):
        return JSONResponse(content={'message': 'Invalid username or password format'}, status_code=400)

    with DBSessionManager() as db_sess:
        if db_sess.query(User).filter_by(username=username).first():
            return JSONResponse(content={'message': 'User with such username already exists'}, status_code=400)
        
        user = User(username=username)
        user.set_password(password)
        user.set_creation_date(datetime.now(timezone.utc))
        if name:
            user.set_name(name)
        user.last_username_edit = datetime.now(timezone.utc)

        db_sess.add(user)
        db_sess.commit()
        
        token = JWT.encode_token(user.id)

        response = JSONResponse(
            content={
                'message': 'User created and logged in',
                'user': user.to_dict(),
            },
            status_code=200
        )
        
        JWT.set_response_cookie(response, token)

        return response


class LoginData(BaseModel):
    username: str
    password: str

@router.post('/login/')
async def login(data: LoginData) -> JSONResponse:
    username = data.username.strip()
    password = data.password.strip()

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.query(User).filter_by(username=username).first()

        if not (user and user.check_password(password)):
            return JSONResponse(content={'message': 'Incorrect credentials'}, status_code=400)
        
        token = JWT.encode_token(user.id)

        response = JSONResponse(
            content={
                'message': 'User logged in',
                'user': user.to_dict(),
            },
            status_code=200
        )
        
        JWT.set_response_cookie(response, token)

        return response


@router.put('/set_name/')
@JWT.require_auth
async def set_user_name(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None
    data = await request.json()
    
    new_name: str | None = data.get('new_name')

    if not new_name:
        return JSONResponse(content={'message': 'New name required'}, status_code=400)
    
    if not User.validate_name(new_name):
        return JSONResponse(content={'message': 'Invalid format for new name'}, status_code=400)

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.get(User, user_id)
        if user is None:
            return JSONResponse(content={'message': 'User doesn\'t exist'}, status_code=400)
        
        user.set_name(new_name)
        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': f'Name successfully changed to {new_name}'}, status_code=200)


@router.put('/change_username/')
@JWT.require_auth
async def change_username(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None
    data: Any = await request.json()

    new_username: str | None = data.get('new_username')
    if not new_username:
        return JSONResponse(content={'Invalid username format'}, status_code=400)

    if not User.validate_username(new_username):
        return JSONResponse(content={'Invalid username format'}, status_code=400)

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.get(User, user_id)

        if user is None:
            return JSONResponse(content={'message': 'User doesn\'t exist'}, status_code=400)

        if user.username == new_username:
            return JSONResponse(content={'message': 'That doesn\'t change the username'}, status_code=400)

        if db_sess.query(User).filter_by(username=new_username).first():
            return JSONResponse(content={'message': 'User with such username already exists'}, status_code=400)
        
        able_to_change = user.able_to_change_username()
        
        if not able_to_change:
            return JSONResponse(content={
                'message': f'You can only update your username once every {UserOptions.USERNAME_UPDATE_LIMIT_HOURS} hours'},
                status_code=401
            )

        user.username = new_username
        user.last_username_edit = datetime.now(timezone.utc)
        
        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': f'Username successfully changed to {new_username}'}, status_code=200)


@router.put('/change_password/')
@JWT.require_auth
async def change_password(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None
    data: Any = await request.json()
    old_password: str | None = data.get('old_password')
    new_password: str | None = data.get('new_password')
    
    if not old_password or not new_password:
        return JSONResponse(content={'message': 'New password and old password required'}, status_code=400)
    
    if old_password == new_password:
        return JSONResponse(content={'message': 'New password must be different than old password'}, status_code=400)
    
    if not User.validate_password(new_password):
        return JSONResponse(content={'message': 'Invalid new password format'}, status_code=400)

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.get(User, user_id)

        if user is None:
            return JSONResponse(content={'message': 'User doesn\'t exist'}, status_code=400)

        if not user.check_password(old_password):
            return JSONResponse(content={'message': 'Old password is incorrect'}, status_code=400)
        
        user.set_password(new_password)

        db_sess.add(user)
        db_sess.commit()

        return JSONResponse(content={'message': 'Password successfully changed'}, status_code=200)


@router.get('/get_user_profile/')
@JWT.require_auth
async def get_user_profile(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None
    username: str | None = request.query_params.get('username')
    if not username:
        return JSONResponse(content={'message': '`username` parameter is required'}, status_code=400)

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.query(User).filter_by(username=username).first()
        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)

        user_followed: bool = db_sess.query(Follow)\
            .filter_by(follower_id=user_id, followed_id=user.id)\
            .first() is not None
            
        user_posts_querry = (
            db_sess.query(Post)
            .filter(Post.user == user)
            .order_by(Post.created_at.desc())
        )
        
        if user.id != user_id:
            user_posts_querry = user_posts_querry.filter(Post.status != 'PRIVATE')
        
        user_posts: list[Post] = user_posts_querry.all()

        content: dict = {
            'message': 'User profile found',
            'user_id': str(user.id),
            'username': user.username,
            'user_name': user.name,
            'num_followers': len(user.followers),
            'num_followed': len(user.follows),
            'posts': [{
                **post.to_dict(req_likes=True),
                'liked_by_user': db_sess.query(Like).filter_by(user_id=user_id, post_id=post.id).first()
                is not None
            } for post in user_posts],
            'pfp_src': user.pfp.image_src if user.pfp else None,
            'user_followed': user_followed
        }

        return JSONResponse(content=content, status_code=200)

@router.get('/get_current_user_profile/')
@JWT.require_auth
def get_current_user_profile(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None

    with DBSessionManager() as db_sess:
        user: User | None = db_sess.get(User, user_id)
        if not user:
            return JSONResponse(content={'message': 'User not found'}, status_code=404)
    
        user_posts: list[Post] = (
            db_sess.query(Post)
            .filter(Post.user == user)
            .order_by(Post.created_at.desc())
            .limit(10)
            .all()
        )
        
        content: dict = {
            'message': 'User profile found',
            'user_id': str(user.id),
            'username': user.username,
            'user_name': user.name,
            'num_followers': len(user.followers),
            'num_followed': len(user.follows),
            'posts': [{
                **post.to_dict(req_likes=True),
                'liked_by_user': db_sess.query(Like).filter_by(user_id=user_id, post_id=post.id).first()
                is not None
            } for post in user_posts],
            'pfp_src': user.pfp.image_src if user.pfp else None
        }
        
        return JSONResponse(content=content, status_code=200)

@router.post('/logout/')
def logout() -> JSONResponse:
    response = JSONResponse(content={'message': 'Successfully logged out'}, status_code=200)
    
    JWT.set_response_cookie(response, '')
    
    return response