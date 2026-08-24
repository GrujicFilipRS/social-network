from io import BytesIO
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, File, Form, Request, UploadFile
from schemas import (
    DTO,
    ExistsGetResponse,
    PostEditRequest,
    PostGetResponse,
    PostMiscResponse,
)
from services.service_models import AuthServiceModel, PostServiceModel

router = APIRouter()


@router.get(
    '/get_post/{post_id}',
    response_model=PostGetResponse
)
@inject
async def get_post(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    return await post_service.get_post(post_id, user_id)


@router.post(
    '/create_post/',
    response_model=PostGetResponse
)
@inject
async def create_post(
    request: Request,
    title: Annotated[str, Form()],
    body: Annotated[str | None, Form()],
    status: Annotated[str, Form()],
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel],
    images: Annotated[list[UploadFile], File()] = []  # noqa: B006
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user_id:
        return PostGetResponse.error('Unauthorized')
    
    image_streams = [
        BytesIO(await image.read())
        for image in images
    ]

    return await post_service.create_post(
        user_id=user_id,
        title=title,
        body=body,
        status=status,
        image_streams=image_streams,
    )


@router.put(
    '/edit_post/{post_id}',
    response_model=DTO
)
@inject
async def edit_post(
    request: Request,
    post_id: UUID,
    edit_request: PostEditRequest,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel],
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
        
    if not user_id:
        return PostGetResponse.error('Unauthorized')
    
    await post_service.edit_post(
        post_id,
        edit_request.title,
        edit_request.body,
        edit_request.status
    )


@router.delete(
    '/delete_post/{post_id}',
    response_model=DTO
)
@inject
async def delete_post(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
            
    if not user_id:
        return PostGetResponse.error('Unauthorized')
    
    return await post_service.delete_post(post_id)

@router.get(
    '/liked_by_current_user/{post_id}',
    response_model=ExistsGetResponse
)
@inject
async def liked_by_current_user(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
                
    if not user_id:
        return PostGetResponse.error('Unauthorized')
        
    return await post_service.post_liked_by_user(post_id, user_id)

@router.get(
    '/misc_data/{post_id}',
    response_model=PostMiscResponse
)
@inject
async def get_misc_data(
    request: Request,
    post_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel]
):
    user_id = auth_service.decode_token(request.cookies.get(auth_service.auth_token_name))
    
    liked_by_current_user: bool = False
    if user_id:
        like_exists_response = await post_service.post_liked_by_user(post_id, user_id)
        if not like_exists_response.success:
            return PostMiscResponse.error(
                like_exists_response.message or\
                'An error while fetching user liked happened'
            )
        
        liked_by_current_user = like_exists_response.exists
    
    # TODO
    num_likes = 1 # await like_service.get_post_num_likes(post_id)
    num_comments = 1 # await comments_service.get_post_num_comments(post_id)
    
    return PostMiscResponse.ok(
        liked_by_current_user,
        num_likes,
        num_comments
    )