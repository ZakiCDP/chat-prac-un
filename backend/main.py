from fastapi import FastAPI
from app.api import auth, chat

app = FastAPI()

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

# Перед запуском таблицы создайте:
# from app.db.database import engine, Base
# import asyncio
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.run(create_tables())