from src.utils.redis_db import redis_client

async def clear_cache():
    patterns = ["yelp:*", "enroll:*", "wom:*", "search:*", "table:*"]

    for pattern in patterns:
        async for key in redis_client.scan_iter(pattern):
            await redis_client.delete(key)