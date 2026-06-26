import json
import asyncio

from sqlalchemy import select

from src.utils.celery_app import celery
from src.utils.db import AsyncSessionLocal
from src.utils.redis_db import redis_client
from src.business_app.models import YelpCompany, EnrollCompany, WordOfMouthCompany


TABLE_MODELS = {"yelp": YelpCompany, "enroll": EnrollCompany, "wfm": WordOfMouthCompany,}


@celery.task(name="process_large_request")
@celery.task(name="process_large_request")
def process_large_request(source, page, limit, sort):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(
            _process_large_request(source, page, limit, sort)
        )
        return result
    finally:
        loop.close()


async def _process_large_request(source, page, limit, sort):
    model = TABLE_MODELS.get(source)

    if not model:
        return

    async with AsyncSessionLocal() as db:
        offset = (page - 1) * limit
        order_by = (model.id.desc() if sort.lower() == "desc" else model.id.asc())
        result = await db.execute(select(model).order_by(order_by).limit(limit).offset(offset))
        rows = result.scalars().all()

        response = {
            "page": page,
            "limit": limit,
            "sort": sort,
            "data": [
                {
                    c.name: getattr(row, c.name)
                    for c in row.__table__.columns
                }
                for row in rows
            ],
        }

        cache_key = f"{source}:{page}:{limit}:{sort}"
        await redis_client.setex(cache_key, 600, json.dumps(response, default=str),)

        return response