import asyncio

from fastapi import HTTPException, status
from src.utils.redis_db import redis_client

RATE_LIMIT_WINDOW = 60


async def check_rate_limit(user_id: int):
    key = f"rate:{user_id}"
    current = await redis_client.get(key)

    if current is None:
        await redis_client.setex(key, RATE_LIMIT_WINDOW, 1)

        return {"status": "ok", "delay": 0}

    count = int(current) + 1
    await redis_client.incr(key)

    if count > 30:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. You are blocked temporarily."
        )

    if count > 20:
        delay = min((count - 20) * 0.1, 2)
        await asyncio.sleep(delay)

        return {"status": "throttled", "delay": delay}

    return {"status": "ok", "delay": 0}