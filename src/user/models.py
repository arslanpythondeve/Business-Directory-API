from sqlalchemy import Column, String, DateTime, Integer, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_name = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    email = Column(String)

    role = Column(String, default="user")