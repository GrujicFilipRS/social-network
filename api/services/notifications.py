from uuid import UUID
from fastapi import APIRouter, Request, WebSocket
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
