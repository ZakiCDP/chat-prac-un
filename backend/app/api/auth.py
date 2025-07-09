from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "tuctucwhoisthis?isyourmom"
ALGORITHM = "HS256"

async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(select(User).where(User.login == login))
    return result.scalars().first()

@router.post("/auth/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_login(db, user.login)
    if existing:
        raise HTTPException(400, "Login exists")
    hashed = pwd_context.hash(user.password)
    new_user = User(login=user.login, password_hash=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_login(db, form.username)
    if not user or not pwd_context.verify(form.password, user.password_hash):
        raise HTTPException(400, "Invalid credentials")
    token = jwt.encode({"sub": user.login}, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}