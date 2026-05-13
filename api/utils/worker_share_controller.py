from redis.asyncio import Redis
from env import Env

class WorkerShareController:
    redis_client: Redis = None
    
    @staticmethod
    def init():
        redis_url = Env.REDIS_URL
        
        WorkerShareController.redis_client = Redis.from_url(redis_url)
        print(f'Redis client initialized successfully at {redis_url}')
    
    @staticmethod
    def set(key: str, value: str):
        if WorkerShareController.redis_client is None:
            raise RuntimeError('WorkerShareController not yet initialized')
        
        WorkerShareController.redis_client.set(key, value)
    
    @staticmethod
    def get(key: str) -> str | None:
        if WorkerShareController.redis_client is None:
            raise RuntimeError('WorkerShareController not yet initialized')
        
        value = WorkerShareController.redis_client.get(key)
        
        return value.decode('utf-8') if value else None
