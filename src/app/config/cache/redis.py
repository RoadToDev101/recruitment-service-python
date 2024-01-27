import redis

# Set up Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


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
