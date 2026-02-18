from datetime import datetime, timezone
from uuid import UUID
from fastapi.responses import JSONResponse

from models.comments import Comment
from models.posts import Post
from db.db_session import DBSessionManager

from utils.jwt_tokens import optional_auth, require_auth
from utils.literals import PostLiterals

from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/get_comment/')
def get_comment(comment_id: UUID | str) -> JSONResponse:
    with DBSessionManager() as db_sess:
        try:
            comment: Comment | None = db_sess.get(Comment, UUID(comment_id))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid comment_id'}, status_code=400)

        if not comment:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)
        
        content: dict[str, str | dict] = {
            'message': 'Comment found',
            'comment': comment.to_dict()
        }

        return JSONResponse(content=content, status_code=200)


@router.post('/post_comment/')
@require_auth
async def post_comment(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    data = await request.json()
    
    if not Comment.validate_creation(data):
        return JSONResponse(content={'message': 'Invalid comment data'}, status_code=400)
    
    body: str = data.get('body').strip()
    post_id: UUID = UUID(data.get('post_id'))
    comment_id: UUID | None = UUID(data.get('comment_id')) if data.get('comment_id') else None

    with DBSessionManager() as db_sess:
        new_comment = Comment(
            body=body,
            post_id=post_id,
            comment_id=comment_id,
            creator_id=user_id,
            commented_at=datetime.now(timezone.utc)
        )

        db_sess.add(new_comment)
        db_sess.commit()

        content: dict = {
            'message': 'Comment posted',
            'comment': new_comment.to_dict()
        }

        return JSONResponse(content=content, status_code=201)


@router.delete('/remove_comment/')
@require_auth
async def delete_comment(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    with DBSessionManager() as db_sess:
        data = await request.json()
        try:
            comment_id = UUID(data.get('comment_id'))
        except ValueError:
            return JSONResponse(content={'message': 'Invalid comment_id'}, status_code=400)

        comment: Comment | None = db_sess.get(Comment, comment_id)

        if comment is None:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)

        if comment.creator_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to delete this comment'}, status_code=401)
        
        db_sess.delete(comment)
        db_sess.commit()

        return JSONResponse(content={'message': 'Comment successfully deleted'}, status_code=200)


@router.get('/get_post_comments/')
@optional_auth
def get_post_comments(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
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

        if post.user_id != user_id:
            return JSONResponse(content={
                'message': 'You are not authorized to view this post'
            }, status_code=401)
        
        return JSONResponse(content=content, status_code=200)