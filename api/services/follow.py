from fastapi.responses import JSONResponse
from fastapi import Header
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

from ..server.db.models.follows import Follow
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

from fastapi import APIRouter

router = APIRouter()


@router.get('/get_follow/')
def get_follow(follow_id: int, req_names: bool = False) -> JSONResponse:
    try:
        db_sess = create_session()

        follow: Follow | None = db_sess.get(Follow, follow_id)

        if follow is None:
            return JSONResponse(content={'message': 'Follow not found'}, status_code=404)
        
        content: dict = {
            'message': 'Follow successfully found',
            'follow': follow.to_dict(req_names=req_names)
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting follow: {e}'}, status_code=400)

    finally:
        db_sess.close()