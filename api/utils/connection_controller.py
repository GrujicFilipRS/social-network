from fastapi import WebSocket
from uuid import UUID


class ConnectionController:
    def __init__(self):
        self.active_connections: dict[UUID, WebSocket] = {}

    def connect(self, user_id: UUID, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: UUID):
        self.active_connections.pop(user_id, None)

    async def send_to_user_if_connected(self, user_id: UUID, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)