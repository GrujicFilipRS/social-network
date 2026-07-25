from fastapi import APIRouter

from .comments import router as comment_router
from .follow_controller import router as follow_router
from .like import router as like_router
from .notifications import router as notifications_router
from .pfp import router as pfp_router
from .post_controller import router as post_router
from .user_controller import router as user_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['user'])
router.include_router(post_router, prefix='/post', tags=['post'])
router.include_router(follow_router, prefix='/follow', tags=['follow'])
router.include_router(like_router, prefix='/like', tags=['like'])
router.include_router(comment_router, prefix='/comment', tags=['comment'])
router.include_router(pfp_router, prefix='/pfp', tags=['pfp'])
router.include_router(notifications_router, prefix='/notifications', tags=['notification'])
