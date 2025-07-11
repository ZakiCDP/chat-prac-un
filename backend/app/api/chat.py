from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from app.core.ws_manager import manager
from app.schemas.message import MessageCreate, MessageRead
from app.models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
from typing import List
from sqlalchemy import select
import app.core.security as secure
import app.models.user as user_c

router = APIRouter()
# Для шифрования messages используем асимметричные ключи, создаем свои ключи или загружаем их

# Генерация ключей для примера (лучше хранить их в файле)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

def encrypt_message(message: str) -> bytes:
    return public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_message(encrypted_bytes: bytes) -> str:
    plaintext = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: user_c.User = Depends(secure.get_current_user), db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Расшифровка сообщения
            encrypted_bytes = base64.b64decode(data)
            message_text = decrypt_message(encrypted_bytes)
            # Сохраняем в базу
            new_msg = Message(user_id=user.id, content=message_text)
            db.add(new_msg)
            await db.commit()
            await db.refresh(new_msg)
            # Шифруем и отправляем всем
            encrypted = encrypt_message(message_text)
            await manager.broadcast(base64.b64encode(encrypted).decode('utf-8'))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/messages", response_model=List[MessageRead])
async def get_messages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message))
    messages = result.scalars().all()
    return messages

@router.post("/messages", response_model=MessageRead)
async def send_message(message_in: MessageCreate, current_user: user_c.User = Depends(secure.get_current_user), db: AsyncSession = Depends(get_db)):
    new_msg = Message(user_id=current_user.id, content=message_in.content)
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    return new_msg