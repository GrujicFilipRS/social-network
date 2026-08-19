from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request
from schemas import (
    DTO,
    ExistsGetResponse,
    FollowCreateRequest,
    FollowGetResponse,
    UserGetResponse,
    UserListResponse,
)
from services.service_models import (
    AuthServiceModel,
    FollowServiceModel,
    NotificationServiceModel,
)

router = APIRouter()


@router.get(
    '/get_follower/{follow_id}',
    response_model=UserGetResponse
)
@inject
async def get_follower(
    follow_id: UUID,
    follow_service: FromDishka[FollowServiceModel]
):
    return await follow_service.get_follower_from_follow(follow_id)

@router.post(
    '/follow_user/',
    response_model=FollowGetResponse
)
@inject
async def follow_user(
    request: Request,
    data: FollowCreateRequest,
    follow_service: FromDishka[FollowServiceModel],
    auth_service: FromDishka[AuthServiceModel],
    notification_service: FromDishka[NotificationServiceModel],
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user_id:
        return DTO.error('Unauthorized')
    
    follow_response = await follow_service.create_follow(user_id, data.to_follow_id)
    
    if follow_response.success and follow_response.follow:
        await notification_service.create_notification(
            receiver_id=data.to_follow_id,
            sender_id=user_id,
            object_type='follow',
            object_id=follow_response.follow.id
        )
    
    return follow_response


@router.delete(
    '/unfollow_user/',
    response_model=DTO
)
@inject
async def unfollow_user(
    request: Request,
    data: FollowCreateRequest,
    follow_service: FromDishka[FollowServiceModel],
    auth_service: FromDishka[AuthServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user_id:
        return DTO.error('Unauthorized')
    
    return await follow_service.remove_follow(user_id, data.to_follow_id)


@router.get(
    '/get_user_follows/',
    response_model=UserListResponse
)
@inject
async def get_user_follows(
    user_id: UUID,
    follow_service: FromDishka[FollowServiceModel]
):
    return await follow_service.get_user_follows(user_id)


@router.get(
    '/get_user_followers/',
    response_model=UserListResponse
)
@inject
async def get_user_followers(
    user_id: UUID,
    follow_service: FromDishka[FollowServiceModel]
):
    return await follow_service.get_user_followers(user_id)


@router.get(
    '/check_if_following/',
    response_model=ExistsGetResponse
)
@inject
async def check_if_following(
    request: Request,
    user_id: UUID,
    follow_service: FromDishka[FollowServiceModel],
    auth_service: FromDishka[AuthServiceModel]
):
    id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    if not id:
        return ExistsGetResponse.error('Unauthorized')
    
    return await follow_service.exists(id, user_id)