from pydantic import BaseModel

class UserCreate(BaseModel):
    login: str
    password: str

class UserRead(BaseModel):
    id: int
    login: str
    joined_at: str

    class Config:
        orm_mode = True