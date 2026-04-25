from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils import JWT
from utils import ConnectionController

router = APIRouter()

@router.websocket('/')
@JWT.required_auth_websocket
async def websocket(
    websocket: WebSocket,
    user_id: UUID | None = None
):
    ConnectionController.connect(user_id, websocket)
    
    try:
        while True:
            await websocket.receive_text() # Keep the connection alive
    except WebSocketDisconnect:
        ConnectionController.disconnect(user_id)