from fastapi.responses import JSONResponse
from fastapi import Header
from typing import Annotated

from fastapi import APIRouter

from ..server.db.models.pfps import PFP
from ..server.db.db_session import create_session

from ..server.utils import jwt_tokens
from .authorization import AuthorizationHeader

router = APIRouter()


@router.get('/get_user_pfp/')
def get_user_pfp(user_id: int) -> JSONResponse:
    try:
        db_sess = create_session()
        pfp: PFP | None = db_sess.query(PFP).filter_by(user_id=user_id).first()

        if pfp is None:
            return JSONResponse(content={'message': 'pfp not found'}, status_code=404)
        
        content: dict = {
            'message': 'Successfully found pfp',
            'image_src': pfp.image_src
        }

        return JSONResponse(content=content, status_code=200)

    except Exception as e:
        return JSONResponse(content={'message': f'Error while getting user pfp: {e}'}, status_code=400)
    
    finally:
        db_sess.close()