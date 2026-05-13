import json
from typing import Any
from fastapi import WebSocket
from uuid import UUID

from .worker_share_controller import WorkerShareController


class ConnectionController:
    active_connections: dict[UUID, WebSocket] = {}

    REDIS_CHANNEL = 'websocket_events'

    @staticmethod
    def connect(user_id: UUID, websocket: WebSocket):
        ConnectionController.active_connections[user_id] = websocket

    @staticmethod
    def disconnect(user_id: UUID):
        ConnectionController.active_connections.pop(user_id, None)

    @staticmethod
    async def send_to_user_if_connected(
        user_id: UUID,
        message: dict[str, Any]
    ) -> bool:
        websocket = ConnectionController.active_connections.get(user_id)

        if not websocket:
            return False

        try:
            await websocket.send_json(message)
            return True
        
        except Exception:
            ConnectionController.disconnect(user_id)
            return False

    @staticmethod
    async def send_to_user(
        user_id: UUID,
        message: dict[str, Any]
    ) -> bool:
        '''
        Sends locally if connected to this worker.
        Otherwise publishes to Redis so another worker can send it.
        '''

        sent = await ConnectionController.send_to_user_if_connected(
            user_id,
            message
        )

        if sent:
            return True

        await WorkerShareController.redis_client.publish(
            ConnectionController.REDIS_CHANNEL,
            json.dumps({
                'user_id': str(user_id),
                'message': message
            })
        )
        
        return False

    @staticmethod
    async def redis_listener():
        '''
        Listens for websocket events from other workers.
        '''

        pubsub = WorkerShareController.redis_client.pubsub()

        await pubsub.subscribe(ConnectionController.REDIS_CHANNEL)

        async for event in pubsub.listen():
            if event['type'] != 'message':
                continue

            payload = json.loads(event['data'])

            await ConnectionController.send_to_user_if_connected(
                UUID(payload['user_id']),
                payload['message']
            )

    def __new__(cls):
        raise ValueError(
            'ConnectionController is a static class and cannot be instantiated'
        )