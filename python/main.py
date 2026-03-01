from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from model.db_model import engine,Base
from model.video_model import video
from model.setting_model import Setting

Base.metadata.create_all(bind=engine)

from routers import video_router,setting_router,service_router, websocket_router
# khoi tao database tu dong
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

app.include_router(websocket_router.router)
app.include_router(video_router.router)
app.include_router(setting_router.router)
app.include_router(service_router.router)
