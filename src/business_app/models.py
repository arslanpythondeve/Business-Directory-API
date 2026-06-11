from sqlalchemy import Column, Integer, String, Text, ForeignKey

from src.utils.db import Base


class CompanyBase:
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(Text)
    phone = Column(Text)
    mobile = Column(Text)
    company_name = Column(Text)
    industry = Column(Text)
    company_website = Column(Text)
    state = Column(Text)
    address = Column(Text)
    country = Column(Text)
    url = Column(Text, unique=True)
    source_website = Column(Text)
    date_added_updated = Column(Text)

    created_by = Column(Integer, ForeignKey("user_table.id"))


class YelpCompany(CompanyBase, Base):
    __tablename__ = "yelp_companies"


class WordOfMouthCompany(CompanyBase, Base):
    __tablename__ = "word_of_mouth"


class EnrollCompany(CompanyBase, Base):
    __tablename__ = "enroll_businesses"