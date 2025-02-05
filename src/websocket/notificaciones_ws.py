from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws/notificaciones/{area_id}")
async def websocket_notificaciones(websocket: WebSocket, area_id: int):
    await manager.connect(websocket, area_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, area_id)
