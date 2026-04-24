from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils import JWT, ConnectionController

router = APIRouter()
controller = ConnectionController()

@router.websocket('/')
@JWT.required_auth_websocket
async def websocket(
    websocket: WebSocket,
    user_id: UUID | None = None
):
    controller.connect(user_id, websocket)
    await websocket.send_text(f'Connected as {user_id}') # Debugging
    
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f'Echo: {message}')
    except WebSocketDisconnect:
        controller.disconnect(user_id)