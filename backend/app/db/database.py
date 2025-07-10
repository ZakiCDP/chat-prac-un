from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# local 
# DATABASE_URL = "postgresql+asyncpg://postgres:G2ty91wx42!dd0@localhost:5432/webchat" 
DATABASE_URL = "postgresql+asyncpg://postgres:G2ty91wx42!dd0@localhost:5432/webchat" 


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session