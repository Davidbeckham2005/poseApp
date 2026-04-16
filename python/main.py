from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from model.db_model import engine,Base
from routers import video_router,setting_router,service_router, websocket_router, user_router, nutrition_router
# Import models to ensure they're registered with Base

Base.metadata.create_all(bind=engine)

# khoi tao database tu dong
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",   # Tauri dev
        "http://127.0.0.1:1420",   # Tauri dev
        "http://localhost:5173",   # Vite dev (nếu có)
        "http://127.0.0.1:5173",   # Vite dev (nếu có)
        "tauri://localhost",
        "http://tauri.localhost",  # Tauri v2
        "https://tauri.localhost", # Tauri v2
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|tauri\.localhost)(:\\d+)?$|^tauri://localhost$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router.router)
app.include_router(video_router.router)
app.include_router(setting_router.router)
# app.include_router(service_router.router)
app.include_router(user_router.router)
app.include_router(nutrition_router.router)
