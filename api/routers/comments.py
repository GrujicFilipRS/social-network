from datetime import datetime, timezone
from uuid import UUID

from db import DBSessionManager
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models import Comment, Post
from schemas import DTO, CommentGetResponse
from services.service_models import AuthServiceModel, CommentServiceModel
from utils import NotificationController, PostLiterals

router = APIRouter()

@router.get(
    '/get_comment/{comment_id}',
    response_model=CommentGetResponse
)
async def get_comment(
    request: Request,
    comment_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    comment_service: FromDishka[CommentServiceModel]
):
    user_id = auth_service.get_user_from_token(request.cookes['auth_token'])
    
    if not user_id:
        return CommentGetResponse.error('Unauthorized')
    
    return comment_service.get_comment(comment_id, user_id)


@router.post(
    '/post_comment/',
    response_model=DTO
)
@inject
async def post_comment(
    request: Request,
    auth_service: FromDishka[AuthServiceModel]
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies['auth_token'])
    
    if not user:
        return DTO.error('Unauthorized')

    data = await request.json()

    if not Comment.validate_creation(data):
        return JSONResponse(content={'message': 'Invalid comment data'}, status_code=400)
    
    body: str = data.get('body').strip()
    post_id: UUID = UUID(data.get('post_id'))
    comment_id: UUID | None = UUID(data.get('comment_id')) if data.get('comment_id') else None

    with DBSessionManager() as db_sess:
        post: Post | None = db_sess.get(Post, post_id)
        if post is None:
            return JSONResponse(content={'message': 'No post found'}, status_code=404)
        
        new_comment = Comment(
            body=body,
            post_id=post.id,
            comment_id=comment_id,
            creator_id=user.id,
            commented_at=datetime.now(timezone.utc)
        )

        db_sess.add(new_comment)
        db_sess.commit()
        
        if post.user_id != user.id:
            await NotificationController.create_notification(
                session=db_sess,
                receiver_id=post.user_id,
                sender_id=user.id,
                object_type='comment',
                object_id=new_comment.id
            )

        content: dict = {
            'message': 'Comment posted',
            'comment': new_comment.to_dict()
        }

        return JSONResponse(content=content, status_code=201)


@router.put('/edit_comment/')
@inject
async def edit_comment(
    request: Request,
    auth_service: FromDishka[AuthServiceModel]
) -> JSONResponse:
    user = auth_service.get_user_from_token(request.cookies['auth_token'])
    
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
    user = auth_service.get_user_from_token(request.cookies['auth_token'])

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
    user = auth_service.get_user_from_token(request.cookies['auth_token'])
    
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