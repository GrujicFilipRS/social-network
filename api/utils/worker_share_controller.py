from redis.asyncio import Redis
from env import Env

class WorkerShareController:
    redis_client: Redis | None = None
    
    @staticmethod
    def init():
        redis_url = Env.REDIS_URL
        
        WorkerShareController.redis_client = Redis.from_url(redis_url, decode_responses=True)
        print(f'Redis client initialized successfully at {redis_url}')
    
    @staticmethod
    async def set(key: str, value: str):
        if WorkerShareController.redis_client is None:
            raise RuntimeError('WorkerShareController not yet initialized')
        
        await WorkerShareController.redis_client.set(key, value)
    
    @staticmethod
    async def get(key: str) -> str | None:
        if WorkerShareController.redis_client is None:
            raise RuntimeError('WorkerShareController not yet initialized')
        
        value: str | None = await WorkerShareController.redis_client.get(key)
        
        return value.strip() if value is not None else None
