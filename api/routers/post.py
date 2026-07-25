from io import BytesIO
from typing import Annotated
from uuid import UUID

from db import DBSessionManager
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, File, Form, Request
from fastapi.responses import JSONResponse
from models import Post
from schemas import PostEditRequest, PostGetResponse
from services.service_models import AuthServiceModel, PostServiceModel
from starlette.datastructures import UploadFile

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
    user_id = auth_service.decode_token(request.cookies['auth_token'])
    
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
    images: Annotated[list[UploadFile], File()] = [],
    auth_service: FromDishka[AuthServiceModel] = Depends(),
    post_service: FromDishka[PostServiceModel] = Depends()
):
    user_id = auth_service.decode_token(request.cookies['auth_token'])
    
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


@router.put('/edit_post/{post_id}')
@inject
async def edit_post(
    request: Request,
    post_id: UUID,
    edit_request: PostEditRequest,
    auth_service: FromDishka[AuthServiceModel],
    post_service: FromDishka[PostServiceModel],
) -> JSONResponse:
    user_id = auth_service.decode_token(request.cookies['auth_token'])
        
    if not user_id:
        return PostGetResponse.error('Unauthorized')
    
    await post_service.edit_post(
        post_id,
        edit_request.title,
        edit_request.body,
        edit_request.status
    )


@router.delete('/delete_post/')
async def delete_post(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    assert user_id is not None

    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            post_id: UUID | None = UUID(data.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        post = db_sess.get(Post, post_id)

        if not post:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)

        if post.user_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to delete this post'}, status_code=401)
        
        db_sess.delete(post)
        db_sess.commit()

        return JSONResponse(content={'message': 'Successfully deleted post'}, status_code=200)
