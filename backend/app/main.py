from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager

from .websocket.manager import ConnectionManager
from .core.database import init_db
from .services.simulation_service import start_simulation, pause_simulation, resume_simulation, trigger_emergency

init_db()
manager = ConnectionManager()

async def broadcast_state(state):
    await manager.broadcast_json(state)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_simulation(broadcast_state)
    yield
    # Shutdown

app = FastAPI(title="VAZHI-AI Traffic Intelligence API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.websocket("/ws/traffic")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/simulation/pause")
def api_pause():
    pause_simulation()
    return {"status": "paused"}

@app.post("/api/simulation/resume")
def api_resume():
    resume_simulation()
    return {"status": "resumed"}
    
@app.post("/api/events/ambulance")
def api_ambulance():
    trigger_emergency()
    return {"status": "ambulance_injected"}
