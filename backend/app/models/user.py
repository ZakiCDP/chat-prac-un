from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)