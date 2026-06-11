import json

from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.cache import clear_cache
from src.utils.redis_db import redis_client
from src.business_app.models import YelpCompany, EnrollCompany, WordOfMouthCompany


TABLE_MODELS = {
    "yelp": YelpCompany,
    "enroll": EnrollCompany,
    "wfm": WordOfMouthCompany
}

async def get_paginated_records(db: AsyncSession, model, page: int, limit: int, sort: str):
    offset = (page - 1) * limit
    order_column = model.id
    order_by = order_column.desc() if sort.lower() == "desc" else order_column.asc()
    query = select(model).order_by(order_by).limit(limit).offset(offset)
    result = await db.execute(query)
    rows = result.scalars().all()

    return {"page": page, "limit": limit, "sort": sort,
            "data": [{c.name: getattr(row, c.name) for c in row.__table__.columns} for row in rows]}

async def get_word_of_mouth_business(db: AsyncSession, page: int, limit: int, sort: str):
    cache_key = f"wom:{page}:{limit}:{sort}"
    cached = await redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    result = await get_paginated_records(db, WordOfMouthCompany, page, limit, sort )
    await redis_client.setex(cache_key, 300, json.dumps(result))
    return result

async def get_yelp_business(db: AsyncSession, page: int, limit: int, sort: str):
    cache_key = f"yelp:{page}:{limit}:{sort}"
    cached = await redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    result = await get_paginated_records(db, YelpCompany, page, limit, sort)
    await redis_client.setex(cache_key, 300, json.dumps(result))
    return result

async def get_enroll_business(db: AsyncSession, page: int, limit: int, sort: str):
    cache_key = f"enroll:{page}:{limit}:{sort}"
    cached = await redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    result = await get_paginated_records(db, EnrollCompany, page, limit, sort)
    await redis_client.setex(cache_key, 300, json.dumps(result))
    return result

async def get_business_by_name(db: AsyncSession, company_name: str):
    cache_key = f"search:{company_name.lower()}"
    cached = await redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    MODELS = {
        "yelp": YelpCompany,
        "enroll": EnrollCompany,
        "word_of_mouth": WordOfMouthCompany
    }

    for source, model in MODELS.items():
        result = await db.execute(select(model).where(model.company_name.ilike(f"%{company_name}%")))
        row = result.scalar_one_or_none()

        if row:
            response = {"source": source, "data": {c.name: getattr(row, c.name) for c in row.__table__.columns}}
            await redis_client.setex(cache_key, 600, json.dumps(response, default=str))
            return response

    raise HTTPException(status_code=404, detail="Business not found")

async def get_business_by_name_from_specific_table(db: AsyncSession, table_name: str, company_name: str):
    cache_key = f"table:{table_name}:{company_name.lower()}"

    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    MODELS = {
        "yelp": YelpCompany,
        "enroll": EnrollCompany,
        "word_of_mouth": WordOfMouthCompany
    }

    model = MODELS.get(table_name)

    if model is None:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table_name}")

    result = await db.execute(select(model).where(model.company_name.ilike(f"%{company_name}%")))
    row = result.scalar_one_or_none()

    if row:
        response = {"source": table_name,"data": {c.name: getattr(row, c.name) for c in row.__table__.columns}}
        await redis_client.setex(cache_key, 600, json.dumps(response, default=str))
        return response

    raise HTTPException(status_code=404, detail="Business not found")

async def create_company(db: AsyncSession, source: str, company, current_user):
    model = TABLE_MODELS.get(source.lower())

    if not model:
        raise HTTPException(status_code=400, detail="Invalid source")

    result = await db.execute(select(model).where(model.url == company.url))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="URL already exists")

    company_data = company.model_dump()
    company_data["created_by"] = current_user.id
    new_company = model(**company_data)
    db.add(new_company)

    await db.commit()
    await clear_cache()
    await db.refresh(new_company)

    return {"message": f"Record added to {source}", "id": new_company.id}

async def update_company(db: AsyncSession, source: str, company_name: str, company, current_user):
    model = TABLE_MODELS.get(source.lower())

    if not model:
        raise HTTPException(status_code=400, detail="Invalid source")

    result = await db.execute(select(model).where(model.company_name == company_name))
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Company not found")

    if current_user.role != "admin" and record.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own records")

    update_data = company.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    await db.commit()
    await clear_cache()
    await db.refresh(record)

    return {"message": "Company updated successfully"}

async def delete_company(db: AsyncSession, source: str, company_name: str, current_user):
    model = TABLE_MODELS.get(source.lower())

    if not model:
        raise HTTPException(status_code=400, detail="Invalid source")

    result = await db.execute(select(model).where(model.company_name == company_name))
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Company not found")

    if current_user.role != "admin" and record.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own records")

    await db.delete(record)
    await db.commit()
    await clear_cache()

    return {"message": "Company deleted successfully"}
