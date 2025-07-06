from fastapi import APIRouter, WebSocket
from core.ws_manager import manager 

router = APIRouter()

# HTTP-методы (CRUD)
@router.get("/messages")
async def get_messages(): 
    pass

@router.post("/messages")
async def send_message():
    pass

@router.delete("/messages/{id}")
async def delete_message(id: int):
    pass

# Пересмотр
# WebSocket-эндпоинт
@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)