from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils import JWT

router = APIRouter()

@router.websocket('/')
@JWT.required_auth_websocket
async def websocket(
    websocket: WebSocket,
    user_id: UUID | None = None
):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'Echo {user_id}: {data}')
    except WebSocketDisconnect:
        print('Client disconnected')