from uuid import UUID

from db import DBSessionManager
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models import Comment, Post
from schemas import CommentCreateRequest, CommentGetResponse
from services.service_models import (
    AuthServiceModel,
    CommentServiceModel,
    NotificationModelServiceModel,
    NotificationServiceModel,
)
from utils import PostLiterals

router = APIRouter()

@router.get(
    '/get_comment/{comment_id}',
    response_model=CommentGetResponse
)
@inject
async def get_comment(
    request: Request,
    comment_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    comment_service: FromDishka[CommentServiceModel]
):
    user_id = auth_service.get_user_from_token(request.cookes[auth_service.auth_token_name])
    
    if not user_id:
        return CommentGetResponse.error('Unauthorized')
    
    return comment_service.get_comment(comment_id, user_id)


@router.post(
    '/post_comment/',
    response_model=CommentGetResponse
)
@inject
async def post_comment(
    request: Request,
    data: CommentCreateRequest,
    auth_service: FromDishka[AuthServiceModel],
    comment_service: FromDishka[CommentServiceModel],
    notification_service: FromDishka[NotificationServiceModel],
    notification_model_service: FromDishka[NotificationModelServiceModel],
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies.get(auth_service.auth_token_name))
    
    if not user:
        return CommentGetResponse.error('Unauthorized')
    
    response = await comment_service.post_comment(
        body=data.body,
        post_id=data.post_id,
        user_id=user.id,
        comment_id=data.comment_id,
        notification_service=notification_service,
        notification_model_service=notification_model_service
    )
    
    return response


@router.put('/edit_comment/')
@inject
async def edit_comment(
    request: Request,
    auth_service: FromDishka[AuthServiceModel]
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies.get(auth_service.auth_token_name))
    
    data = await request.json()
    try:
        comment_id = UUID(data.get('comment_id'))
    except ValueError:
        return JSONResponse(content={'message': 'Invalid comment_id'}, status_code=400)
    
    if not Comment.validate_body(data):
        return JSONResponse(content={'message': 'Invalid comment data'}, status_code=400)
    
    body: str = data.get('body')
    
    with DBSessionManager() as db_sess:
        comment: Comment | None = db_sess.get(Comment, comment_id)

        if comment is None:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)

        if comment.creator != user:
            return JSONResponse(content={'message': 'You are not authorized to delete this comment'}, status_code=401)
        
        comment.body = body
        
        db_sess.commit()
        
    return JSONResponse(content={'message': 'Successfully edited comment'}, status_code=200)

@router.delete('/remove_comment/')
@inject
async def delete_comment(
    request: Request,
    auth_service: FromDishka[AuthServiceModel]
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies.get(auth_service.auth_token_name))

    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            comment_id = UUID(data.get('comment_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid comment_id'}, status_code=400)

        comment: Comment | None = db_sess.get(Comment, comment_id)

        if comment is None:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)

        if comment.creator != user:
            return JSONResponse(content={'message': 'You are not authorized to delete this comment'}, status_code=401)
        
        db_sess.delete(comment)
        db_sess.commit()

        return JSONResponse(content={'message': 'Comment successfully deleted'}, status_code=200)


@router.get('/get_post_comments/')
@inject
def get_post_comments(
    request: Request,
    auth_service: FromDishka[AuthServiceModel]
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies.get(auth_service.auth_token_name))
    
    with DBSessionManager() as db_sess:
        try:
            post_id: UUID | None = UUID(request.query_params.get('post_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid post_id'}, status_code=400)

        post: Post | None = db_sess.get(Post, post_id)

        if post is None:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        content: dict = {
            'message': 'Successfully gotten comments of post',
            'comments': [comm.to_dict() for comm in post.comments]
        }

        if post.status == PostLiterals.PUBLIC:
            return JSONResponse(content=content, status_code=200)

        if post.user != user:
            return JSONResponse(content={
                'message': 'You are not authorized to view this post'
            }, status_code=401)
        
        return JSONResponse(content=content, status_code=200)