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
    await websocket.send_text(f'Connected as {user_id}') # Debugging
    
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f'Echo: {message}')
    except WebSocketDisconnect:
        ConnectionController.disconnect(user_id)