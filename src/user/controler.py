from datetime import datetime, timedelta

import jwt
from sqlalchemy import select
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Request

from src.user.models import UserModel
from src.utils.settings import settings
from src.user.dtos import UserSchema, LoginSchema

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def registration(body: UserSchema, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.user_name == body.user_name))
    is_user = result.scalar_one_or_none()

    if is_user:
        raise HTTPException(400, detail="This user already exist ..")

    result = await db.execute(select(UserModel).where(UserModel.email == body.email))
    is_user = result.scalar_one_or_none()

    if is_user:
        raise HTTPException(400, detail="This email already exist ..")

    hash_password = get_password_hash(body.password)
    new_user = UserModel(name=body.name, user_name=body.user_name, hash_password=hash_password,
                         email=body.email, role="user")
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)
    return new_user

async def user_login(body: LoginSchema, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.user_name == body.user_name))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Name!")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Password!")

    exp_time = (datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    token = jwt.encode(
        {
            "id": user.id,
            "username": user.user_name,
            "exp": exp_time.timestamp()
        },
        settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return {"token": token}


async def is_authenticated(request: Request, db: AsyncSession):
    try:
        token = request.headers.get("authenticated", "")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")

        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("id")

        result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")

        return user

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")