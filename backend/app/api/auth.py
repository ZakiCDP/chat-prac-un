from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "shish"  # замените на свой секрет
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(
        select(User).where(User.login == login)
    )
    return result.scalars().first()

@router.post("/auth/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_login(db, user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already exists")
    hashed_password = get_password_hash(user.password)
    new_user = User(login=user.login, password_hash=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_login(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    token = jwt.encode({"sub": user.login}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}