from fastapi import FastAPI

def configure_routing(app: FastAPI) -> None:
    from .services.user import router as user_router
    from .services.post import router as post_router
    from .services.follow import router as follow_router
    from .services.like import router as like_router

    app.include_router(user_router, prefix='/user', tags=['user'])
    app.include_router(post_router, prefix='/post', tags=['post'])
    app.include_router(follow_router, prefix='/follow', tags=['follow'])
    app.include_router(like_router, prefix='/like', tags=['like'])