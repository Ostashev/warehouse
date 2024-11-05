import redis
import json

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_cached_data(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cached_data(key: str, value, expiration: int = 300):
    redis_client.set(key, json.dumps(value), ex=expiration)
