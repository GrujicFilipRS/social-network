from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from schemas import PhotoListResponse
from services.service_models import AuthServiceModel, PhotoServiceModel

router = APIRouter()

@router.get(
    '/get_post_photos/{post_id}',
    response_model=PhotoListResponse
)
@inject
async def get_post_photos(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    photo_service: FromDishka[PhotoServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    return await photo_service.get_post_photos(post_id, user_id)