from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Request, WebSocket
from schemas import DTO, NotificationListResponse
from services.service_models import AuthServiceModel, NotificationModelServiceModel
from utils import ConnectionController

router = APIRouter()


@router.websocket('/')
@inject
async def websocket(
    websocket: WebSocket,
    auth_service: FromDishka[AuthServiceModel]
):
    cookie_header = websocket.headers.get('cookie')
    if not cookie_header:
        return

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
    
    return await notification_service.get_unread_notifications(user_id)
        

@router.post(
    '/read_notification/{notification_id}/',
    response_model=DTO
)
@inject
async def read_notification(
    request: Request,
    notification_id: UUID,
    auth_service: FromDishka[AuthServiceModel],
    notification_service: FromDishka[NotificationModelServiceModel]
):
    user_id = auth_service.decode_token(request.cookies['auth_token'])
    
    return await notification_service.read_notification(notification_id, user_id)