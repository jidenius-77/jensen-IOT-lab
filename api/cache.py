import json
import os
import redis

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


def get_latest_from_cache(device_id):
    
    data = client.get(f"latest:{device_id}")
    if data:
        return json.loads(data)

    return None


def set_latest_in_cache(device_id, measurement):
    
    if measurement is not None:
        client.set(f"latest:{device_id}", json.dumps(measurement))
