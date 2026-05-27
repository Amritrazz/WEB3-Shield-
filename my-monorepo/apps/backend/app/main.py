import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from app.db.postgres import init_db

# 1. Initialize FastAPI Application Core
app = FastAPI(title="Web3-Shield Backend Core Engine")

# 2. Configure CORS Security Policies
# Allows your Next.js dashboard (port 3000) to fetch statistics and connect to WebSockets securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. WebSocket Connection Layer Manager
class ConnectionManager:
    def __init__(self):
        # Keeps track of all actively connected browser tabs and monitoring nodes
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        print(f"[WebSocket] New monitoring client established connection node. Total: {len(self.active)}")

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)
            print(f"[WebSocket] Client disconnected from intercept channel. Total: {len(self.active)}")

    async def broadcast(self, message: dict):
        # Dispatches live alert packages to all listening analyst dashboards instantly
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                # If a client dropped connection abruptly, pass safely to prevent broadcast breaking
                pass

manager = ConnectionManager()


# 4. Global Subsystem Lifecycle Automation Event Hooks
@app.on_event('startup')
async def startup():
    """Wakes up the PostgreSQL async driver engine to provision tables on startup."""
    await init_db()


# 5. REST API Standard Routing Endpoints
@app.get("/")
def read_root():
    """Operational health monitoring heartbeat diagnostic check."""
    return {
        "status": "healthy", 
        "service": "Web3-Shield AI Engine",
        "subsystems": {"db": "asyncpg_connected", "websockets": "listening"}
    }


# 6. WebSocket Streaming Intercept Pipeline Channel
@app.websocket("/ws/threats")
async def threat_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keeps the WebSocket communication tunnel alive to await background broadcast vectors
            await websocket.receive_text()  
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# 7. Core Action Trigger: Broadcast System Intercept Function
async def broadcast_threat(scan_result: dict):
    """Utility function to invoke from scan handlers to alert all dashboards when risk bounds cross 60%."""
    if scan_result.get("risk_score", 0) > 60:
        await manager.broadcast({
            "type": "threat_detected",
            "data": scan_result,
            "ts": datetime.datetime.utcnow().isoformat()
        })