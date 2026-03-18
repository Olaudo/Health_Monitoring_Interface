"""
WebSocket connection manager.
Connections are grouped by hospital_id so a broadcast
only reaches dashboards within the same hospital.
"""
import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # { hospital_id: set of WebSocket connections }
        self.rooms: dict[int, set[WebSocket]] = {}

    async def connect(self, hospital_id: int, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(hospital_id, set()).add(ws)

    def disconnect(self, hospital_id: int, ws: WebSocket):
        if hospital_id in self.rooms:
            self.rooms[hospital_id].discard(ws)

    async def broadcast(self, hospital_id: int, data: dict):
        """Send a JSON event to all dashboards in this hospital."""
        dead = set()
        for ws in self.rooms.get(hospital_id, set()):
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(hospital_id, ws)

    def connected_count(self, hospital_id: int) -> int:
        return len(self.rooms.get(hospital_id, set()))
