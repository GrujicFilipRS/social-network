from uuid import UUID
from fastapi.responses import JSONResponse

from server.db.models.comments import Comment
from server.db.models.posts import Post
from server.db.db_session import create_session

from server.utils.jwt_tokens import optional_auth, require_auth

from fastapi import APIRouter, Request
import literals

router = APIRouter()


@router.get('/get_comment/')
def get_comment(comment_id: int) -> JSONResponse:
    try:
        db_sess = create_session()
        
        comment: Comment | None = db_sess.get(Comment, comment_id)

        if not comment:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)
        
        content: dict[str, str | dict] = {
            'message': 'Comment found',
            'comment': comment.to_dict()
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting comment: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.post('/post_comment/')
@require_auth
async def post_comment(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        data = await request.json()
        db_sess = create_session()
        
        new_comment = Comment(
            body=data.get('body'),
            post_id=UUID(data.get('post_id')),
            comment_id=UUID(data.get('comment_id')) if data.get('comment_id') else None,
            creator_id=user_id
        )

        db_sess.add(new_comment)
        db_sess.commit()

        content: dict = {
            'message': 'Comment posted',
            'comment': new_comment.to_dict()
        }

        return JSONResponse(content=content, status_code=201)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting comment: {e}'}, status_code=400)

    finally:
        db_sess.close()


@router.delete('/remove_comment/')
@require_auth
async def delete_comment(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        comment_id = UUID((await request.json()).get('comment_id'))

        db_sess = create_session()
        comment: Comment | None = db_sess.get(Comment, comment_id)

        if comment is None:
            return JSONResponse(content={'message': 'Comment not found'}, status_code=404)

        if comment.creator_id != user_id:
            return JSONResponse(content={'message': 'You are not authorized to delete this comment'}, status_code=401)
        
        db_sess.delete(comment)
        db_sess.commit()

        return JSONResponse(content={'message': 'Comment successfully deleted'}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while deleting comment: {e}'}, status_code=400)
    
    finally:
        db_sess.close()


@router.get('/get_post_comments/')
@optional_auth
def get_post_comments(
    request: Request,
    user_id: UUID | None = None
) -> JSONResponse:
    try:
        db_sess = create_session()
        
        post_id = UUID(request.query_params.get('post_id'))
        post: Post | None = db_sess.get(Post, post_id)
        
        if post is None:
            return JSONResponse(content={'message': 'Post not found'}, status_code=404)
        
        content: dict = {
            'message': 'Successfully gotten comments of post',
            'comments': [comm.to_dict() for comm in post.comments]
        }

        if post.status == literals.PostLiterals.PUBLIC:
            return JSONResponse(content=content, status_code=200)

        if post.user_id != user_id:
            return JSONResponse(content={
                'message': 'You are not authorized to view this post'
            }, status_code=401)
        
        return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting post comments: {e}'}, status_code=400)
    
    finally:
        db_sess.close()