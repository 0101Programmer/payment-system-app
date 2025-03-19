from .config import Config
import asyncio_redis

async def get_redis():
    host = Config.REDIS_HOST
    port = Config.REDIS_PORT
    return await asyncio_redis.Connection.create(host=host, port=int(port))