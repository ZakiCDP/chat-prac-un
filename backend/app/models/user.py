from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)