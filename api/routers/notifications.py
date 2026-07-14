from uuid import UUID
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import inject, FromDishka

from models import Notification
from utils import JWT, ConnectionController
from db import DBSessionManager
from services.service_models import AuthServiceModel, NotificationModelServiceModel
from schemas import NotificationListResponse

router = APIRouter()


@router.websocket('/')
@inject
async def websocket(
    websocket: WebSocket,
    auth_service: FromDishka[AuthServiceModel]
):
    cookie_header = websocket.headers.get('cookie')
    if not cookie_header:
        return None

    cookies = dict(
        item.strip().split('=', 1)
        for item in cookie_header.split(';')
    )
    
    user_id = auth_service.decode_token(cookies['auth_token'])

    await websocket.accept()

    ConnectionController.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception as e:
        print('WS ERROR:', e)


@router.get(
    '/get_unread_notifications/',
    response_model=NotificationListResponse
)
@inject
async def get_unread_notifications(
    request: Request,
    auth_service: FromDishka[AuthServiceModel],
    notification_service: FromDishka[NotificationModelServiceModel]
):
    user_id = auth_service.decode_token(request.cookies['auth_token'])
    
    return notification_service.get_unread_notifications(user_id)
        

@router.post('/read_notification/{notification_id}/')
@JWT.require_auth
async def read_notification(
    request: Request,
    notification_id: UUID,
    user_id: UUID | None = None
):
    assert user_id is not None

    with DBSessionManager() as db_sess:
        notification = db_sess.query(Notification).get(notification_id)

        if not notification:
            return JSONResponse(status_code=404, content={'error': 'Notification not found'})

        notification.seen = True
        db_sess.commit()

        return JSONResponse(status_code=200, content={'message': 'Notification marked as read'})