import jwt
from sqlalchemy import select
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, HTTPException, status, Depends

from src.utils.db import get_db
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.rate_limit import check_rate_limit


async def is_authenticated(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = request.headers.get("authenticated", "")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")

        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = data.get("id")
        await check_rate_limit(user_id)

        result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")

        return user

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")