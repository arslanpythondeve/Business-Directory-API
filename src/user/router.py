from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Request

from src.user import controler
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema

user_routes = APIRouter(prefix="/user")


@user_routes.post("/registration", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def registration(body: UserSchema, db: AsyncSession = Depends(get_db)):
    return await controler.registration(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
async def login(body: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await controler.user_login(body, db)

@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def is_auth(request: Request, db: AsyncSession = Depends(get_db)):
    return await controler.is_authenticated(request, db)