import redis
from fastapi import HTTPException

REDIS_URL = "redis://localhost:6379"

try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
except redis.RedisError:
    redis_client = None

def get_redis():
    if not redis_client:
        raise HTTPException(status_code=500,
            detail={"error": "Redis is unavailable"}
        )
    return redis_client

def check_rate_limit(user_id: str):
    redis = get_redis()

    key = f"rate_limit:{user_id}"

    current = redis.incr(key)

    if current == 1:
        redis.expire(key, 60)

    if current > 10:
        raise HTTPException(status_code=429, detail={"error": "Rate limit exceeded"}
    )

def cache_job_result(job_id: str, result: str):
    redis = get_redis()
    key = f"job_result:{job_id}"
    redis.setex(key, 300, result)

def get_cached_result(job_id: str):
    redis = get_redis()
    key = f"job_result:{job_id}"
    return redis.get(key)

