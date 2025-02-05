from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, area_id: int):
        await websocket.accept()
        if area_id not in self.active_connections:
            self.active_connections[area_id] = []
        self.active_connections[area_id].append(websocket)

    def disconnect(self, websocket: WebSocket, area_id: int):
        if area_id in self.active_connections:
            self.active_connections[area_id].remove(websocket)
            if not self.active_connections[area_id]:
                del self.active_connections[area_id]

    async def notify_area(self, area_id: int, data: dict):
        if area_id in self.active_connections:
            for connection in self.active_connections[area_id]:
                await connection.send_json(data)

manager = ConnectionManager()
