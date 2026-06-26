from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.user.models import UserModel
from src.business_app import controler
from celery.result import AsyncResult
from src.utils.celery_app import celery
from src.utils.helper import is_authenticated
from src.business_app.dtos import CompanyCreate, BusinessQueryParams

business_routes = APIRouter(prefix="/business")


@business_routes.get("/word_of_mouth")
async def get_business(db: AsyncSession = Depends(get_db), params: BusinessQueryParams = Depends(),
    user: UserModel = Depends(is_authenticated)):

    return await controler.get_word_of_mouth_business(db, params.page, params.limit, params.sort)


@business_routes.get("/yelp")
async def get_business(db: AsyncSession = Depends(get_db), params: BusinessQueryParams = Depends(),
    user: UserModel = Depends(is_authenticated)):

    return await controler.get_yelp_business(db, params.page, params.limit, params.sort)


@business_routes.get("/enroll")
async def get_business(db: AsyncSession = Depends(get_db), params: BusinessQueryParams = Depends(),
    user: UserModel = Depends(is_authenticated)):

    return await controler.get_enroll_business(db, params.page, params.limit, params.sort)


@business_routes.get("/search/{company_name}")
async def get_business(company_name: str, db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(is_authenticated)):

    return await controler.get_business_by_name(db, company_name)


@business_routes.get("/table/{table}/{company_name}")
async def get_business_from_table(table: str, company_name: str, db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(is_authenticated)):

    return await controler.get_business_by_name_from_specific_table(db, table, company_name)


@business_routes.put("/{source}/{company_name}/update")
async def update_company(source: str, company_name: str, company: CompanyCreate, db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(is_authenticated)):

    return await controler.update_company(db, source, company_name, company, user)


@business_routes.post("/{source}/create")
async def create_company(source: str, company: CompanyCreate, db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(is_authenticated)):

    return await controler.create_company(db, source, company, user)


@business_routes.delete("/{source}/{company_name}/del")
async def delete_company(source: str, company_name: str, db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(is_authenticated)):

    return await controler.delete_company(db, source, company_name, user)

@business_routes.get("/task/{task_id}")
async def get_task(task_id: str):
    task = AsyncResult(task_id, app=celery)

    if task.state == "PENDING":
        return {"status": "Processing"}

    elif task.state == "SUCCESS":
        return {"status": "Completed", "data": task.result}

    elif task.state == "FAILURE":
        return {"status": "Failed"}

    return {"status": task.state}