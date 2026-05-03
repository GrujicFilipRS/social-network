from typing import Any
from fastapi import WebSocket
from uuid import UUID


class ConnectionController:
    active_connections: dict[UUID, WebSocket] = {}

    @staticmethod
    def connect(user_id: UUID, websocket: WebSocket):
        ConnectionController.active_connections[user_id] = websocket

    @staticmethod
    def disconnect(user_id: UUID):
        ConnectionController.active_connections.pop(user_id, None)

    @staticmethod
    async def send_to_user_if_connected(user_id: UUID, message: dict[str, Any]):
        websocket = ConnectionController.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)
    
    def __new__(cls):
        return ValueError('ConnectionController is a static class and cannot be instantiated')
