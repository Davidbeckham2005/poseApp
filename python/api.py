from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from controller.controller import process, show_cam
# schemas
from schemas.video_schemas import Delete_Video_Schemas, Delete_List_video_Schemas, Video_Schemas, Webcam_Schemas
# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, relationship
# model
from model.video_model import video
from model.setting_model import Setting
from model.db_model import get_db,engine,Base
# crud
from crud.crud_setting import update_setting, read_setting
from crud.crud_video import create_video , delete_video, delete_list_video,read_video, read_all_video
# khoi tao database tu
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

@app.post("/addVideo/")
async def add_Video(input: Video_Schemas, db: Session = Depends(get_db)):
    update_setting(input,db)
    result = process(input)
    record = create_video(result,db)
    return record

@app.delete("/deleteVideo/")
async def delete_video_route(data: Delete_Video_Schemas,db: Session = Depends(get_db) ):
    return delete_video(data,db)

@app.delete("/deleteVideos/")
async def delete_list_video_route(data: Delete_List_video_Schemas,db: Session = Depends(get_db) ):
    return delete_list_video(data,db)

@app.get("/get_setting")
def get_setting(db: Session = Depends(get_db)):
   return read_setting(db)

@app.get("/get_video/{output_path}")
def get_video(output_path:str, db: Session = Depends(get_db)):
    return read_video(output_path,db)

@app.get("/get_video/")
def get_all_video(db:Session = Depends(get_db)):
    return read_all_video(db)

@app.post("/show_webcam/")
def show_webcam(input: Webcam_Schemas, db: Session = Depends(get_db)):
    show_cam(input)
