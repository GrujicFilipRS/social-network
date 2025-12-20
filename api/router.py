from fastapi import FastAPI

def configure_routing(app: FastAPI) -> None:
    from services.user import router as user_router
    from services.post import router as post_router
    from services.follow import router as follow_router
    from services.like import router as like_router
    from services.comments import router as comment_router
    from services.pfp import router as pfp_router

    app.include_router(user_router, prefix='/user', tags=['user'])
    app.include_router(post_router, prefix='/post', tags=['post'])
    app.include_router(follow_router, prefix='/follow', tags=['follow'])
    app.include_router(like_router, prefix='/like', tags=['like'])
    app.include_router(comment_router, prefix='/comment', tags=['comment'])
    app.include_router(pfp_router, prefix='/pfp', tags=['pfp'])