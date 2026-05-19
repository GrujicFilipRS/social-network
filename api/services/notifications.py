from uuid import UUID
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import JSONResponse
from models import Notification
from utils import JWT, ConnectionController
from db import DBSessionManager

router = APIRouter()


@router.websocket('/')
@JWT.required_auth_websocket
async def websocket(websocket: WebSocket, user_id: UUID):
    await websocket.accept()

    ConnectionController.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception as e:
        print('WS ERROR:', e)


@router.get('/get_unread_notifications/')
@JWT.require_auth
async def get_unread_notifications(
    request: Request,
    user_id: UUID | None = None
):
    assert user_id is not None

    NOTIFICATION_LIMIT = 10

    with DBSessionManager() as db_sess:
        notifications = (
            db_sess.query(Notification)
            .filter_by(receiver_id=user_id, seen=False)
            .order_by(Notification.received_at.desc())
            .limit(NOTIFICATION_LIMIT)
            .all()
        )

        return [
            notification.to_dict()
            for notification in notifications
        ]
        

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