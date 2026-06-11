from fastapi import FastAPI

from src.utils.db import init_db
from src.business_app.router import business_routes
from src.user.router import user_routes

app = FastAPI(title="This is my Business Directory")


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(business_routes)
app.include_router(user_routes)