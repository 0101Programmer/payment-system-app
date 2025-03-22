from .config import Config
import asyncio_redis

async def get_redis():
    host = Config.REDIS_HOST if int(Config.USE_DOCKER) else Config.NO_DOCKER_REDIS_HOST
    port = Config.REDIS_PORT if int(Config.USE_DOCKER) else Config.NO_DOCKER_REDIS_PORT
    return await asyncio_redis.Connection.create(host=host, port=int(port))