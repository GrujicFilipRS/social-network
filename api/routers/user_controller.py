from uuid import UUID
from dishka.integrations.fastapi import FromDishka, inject
from fastapi.responses import JSONResponse
from fastapi import Request, Response

from schemas import (
    UserGetResponse,
    UserRegistrationRequest,
    UserLoginRequest,
    DTO,
    SetNameRequest,
    UserChangeUsernameRequest,
    UserChangePasswordRequest
)
from services.service_models import UserServiceModel
from models import Like, User, Follow, Post
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
):
    response = await user_service.get_user(user_id)
    return response


@router.get(
    '/get_current_user/',
    response_model=UserGetResponse
)
@inject
async def get_current_user(
    request: Request,
    user_service: FromDishka[UserServiceModel]
):
    user_id = JWT.get_id_from_request(request)
    
    if not user_id:
        return UserGetResponse.error('Unauthorized')
    
    response = await user_service.get_user(user_id)
    return response


@router.post(
    '/register/',
    response_model=UserGetResponse
)
@inject
async def register(
    data: UserRegistrationRequest,
    response: Response,
    user_service: FromDishka[UserServiceModel]
):
    result = await user_service.register(data.username, data.password, data.name)
    
    if result.user:
        JWT.set_response_cookie(response, JWT.encode_token(UUID(result.user.id)))
    
    return result


@router.post(
    '/login/',
    response_model=UserGetResponse
)
@inject
async def login(
    data: UserLoginRequest,
    response: Response,
    user_service: FromDishka[UserServiceModel]
):
    result = await user_service.log_in(data.username, data.password)
    
    if result.user:
        JWT.set_response_cookie(response, JWT.encode_token(UUID(result.user.id)))
    
    return result


@router.put(
    '/set_name/',
    response_model=DTO
)
@inject
async def set_user_name(
    request: Request,
    data: SetNameRequest,
    user_service: FromDishka[UserServiceModel]
):
    user_id = JWT.get_id_from_request(request)
    response = await user_service.set_name(user_id, data.new_name)
    return response


@router.put(
    '/change_username/',
    response_model=DTO
)
@inject
async def change_username(
    request: Request,
    data: UserChangeUsernameRequest,
    user_service: FromDishka[UserServiceModel]
):
    user_id = JWT.get_id_from_request(request)
    response = await user_service.change_username(user_id, data.new_username)
    
    return response


@router.put('/change_password/')
@inject
async def change_password(
    request: Request,
    data: UserChangePasswordRequest,
    user_service: FromDishka[UserServiceModel]
):
    user_id = JWT.get_id_from_request(request)
    
    response = await user_service.change_password(user_id, data.old_password, data.new_password)
    return response


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