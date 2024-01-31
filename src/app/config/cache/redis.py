from app.config.logging.logging_config import g_logger
import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Redis client
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0,
    decode_responses=True,
)

# Check connection
try:
    if redis_client.ping():
        g_logger.info(f'Connected to Redis server on port {os.getenv("REDIS_PORT")}')
except redis.ConnectionError:
    g_logger.error("Error connecting to Redis server: ", exc_info=True)
    exit(1)


async def get_redis_cache(key: str):
    try:
        return redis_client.get(key)
    except redis.RedisError:
        return None


async def set_redis_cache(key: str, value: str, ex_seconds: int = 3600):
    try:
        redis_client.set(key, value, ex=ex_seconds)
    except redis.RedisError:
        pass