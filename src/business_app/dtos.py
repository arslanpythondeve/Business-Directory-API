from typing import Literal, Optional
from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_website: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    url: str
    source_website: Optional[str] = None
    date_added_updated: Optional[str] = None


class BusinessQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
    sort: Literal["asc", "desc"] = "asc"