# app/services/queue.py
import json
import redis
from app.config import settings

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)

QUEUE_KEY = "events_queue"

def push_event(event_dict: dict) -> None:
    r.rpush(QUEUE_KEY, json.dumps(event_dict, default=str))

def pop_batch(max_items: int = 500) -> list[dict]:
    pipe = r.pipeline()
    pipe.lrange(QUEUE_KEY, 0, max_items - 1)
    pipe.ltrim(QUEUE_KEY, max_items, -1)
    items, _ = pipe.execute()
    return [json.loads(i) for i in items]