from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request
from schemas import DTO, LikeGetResponse
from services.service_models import AuthServiceModel, LikeServiceModel

router = APIRouter()


@router.get(
    '/get_like/{id}',
    response_model=LikeGetResponse
)
@inject
async def get_like(
    request: Request,
    id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    like_service: FromDishka[LikeServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    return await like_service.get_like(id, user_id)


@router.post(
    '/like_post/{post_id}',
    response_model=DTO
)
@inject
async def like_post(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    like_service: FromDishka[LikeServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user_id:
        return DTO.error('Unauthorized')
    
    return await like_service.like_post(post_id, user_id)
    

@router.delete(
    '/unlike_post/{post_id}',
    response_model=DTO
)
@inject
async def unlike_post(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    like_service: FromDishka[LikeServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
        
    if not user_id:
        return DTO.error('Unauthorized')
    
    return await like_service.unlike_post(post_id, user_id)
