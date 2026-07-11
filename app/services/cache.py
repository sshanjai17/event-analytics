import redis
from app.config import settings

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)

VALID_KEYS = "valid_api_keys"
TTL = 300  # seconds

def is_valid_api_key(api_key: str, db_lookup) -> bool:
    if r.sismember(VALID_KEYS, api_key):
        return True
    if db_lookup(api_key):
        r.sadd(VALID_KEYS, api_key)
        r.expire(VALID_KEYS, TTL)
        return True
    return False