from fastapi import FastAPI, WebSocket # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import true # type: ignore
from model.db_model import engine,Base
import json, asyncio
# routers
from routers import video_router,setting_router,service_router
# khoi tao database tu dong
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",   # Tauri dev
        "http://localhost:5173",   # Vite dev (nếu có)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await asyncio.sleep(2)  
        result = {
            "rep": 5,
            "state": "down"
        }
        await websocket.send_text(json.dumps(result))
app.include_router(video_router.router)
app.include_router(setting_router.router)
app.include_router(service_router.router)
