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
    UserChangePasswordRequest,
    UserProfileResponse
)
from services.service_models import UserServiceModel, FollowServiceModel, PostServiceModel

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


@router.get(
    '/get_user_profile/',
    response_model=UserProfileResponse
)
@inject
async def get_user_profile(
    request: Request,
    username: str,
    user_service: FromDishka[UserServiceModel],
    follow_service: FromDishka[FollowServiceModel],
    post_service: FromDishka[PostServiceModel]
):  
    user_id = JWT.get_id_from_request(request)
    
    user_get_response = await user_service.get_user_by_username(username)
    user = user_get_response.user
    
    if not user:
        return UserProfileResponse.error('User not found')
    
    user_followed = await follow_service.exists(user_id, user.id)
    
    user_followers_response = await follow_service.get_user_followers(user.id)
    if not user_followers_response.success:
        return UserProfileResponse.error(user_followers_response.message)
    
    user_follows_response = await follow_service.get_user_followers(user.id)
    if not user_follows_response.success:
        return UserProfileResponse.error(user_follows_response.message)
    
    num_followers = len(user_followers_response.follows)
    num_follows = len(user_followers_response.follows)
    
    posts_response = await post_service.get_user_posts(user.id, user.id != user_id)
    if not posts_response.success:
        UserProfileResponse.error(posts_response.message)
    
    return UserProfileResponse.ok(
        user_get_response.user,
        user_followed.exists,
        num_followers,
        num_follows,
        posts_response.posts
    )
    

@router.get(
    '/get_current_user_profile/',
    response_model=UserProfileResponse
)
@inject
async def get_current_user_profile(
    request: Request,
    user_service: FromDishka[UserServiceModel],
    follow_service: FromDishka[FollowServiceModel],
    post_service: FromDishka[PostServiceModel]
):
    user_id = JWT.get_id_from_request(request)
    
    user_get_response = await user_service.get_user(user_id)
    user = user_get_response.user
    
    if not user:
        return UserProfileResponse.error('User not found')
    
    user_followed = await follow_service.exists(user_id, user.id)
    
    user_followers_response = await follow_service.get_user_followers(user.id)
    if not user_followers_response.success:
        return UserProfileResponse.error(user_followers_response.message)
    
    user_follows_response = await follow_service.get_user_followers(user.id)
    if not user_follows_response.success:
        return UserProfileResponse.error(user_follows_response.message)
    
    num_followers = len(user_followers_response.follows)
    num_follows = len(user_followers_response.follows)
    
    posts_response = await post_service.get_user_posts(user.id)
    if not posts_response.success:
        UserProfileResponse.error(posts_response.message)
    
    return UserProfileResponse.ok(
        user_get_response.user,
        user_followed.exists,
        num_followers,
        num_follows,
        posts_response.posts
    )
    

@router.post(
    '/logout/',
    response_model=DTO
)
def logout() -> JSONResponse:
    response = JSONResponse(content=DTO.ok().__dict__, status_code=200)
    
    JWT.set_response_cookie(response, '')
    
    return response