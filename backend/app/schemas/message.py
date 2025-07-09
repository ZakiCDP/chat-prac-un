from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: str

    class Config:
        orm_mode = True