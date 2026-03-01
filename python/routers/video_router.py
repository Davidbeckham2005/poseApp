from fastapi import APIRouter # type: ignore
from controller.controller import process
# schemas
from schemas.video_schemas import Delete_Video_Schemas, Delete_List_video_Schemas, Video_Schemas, Webcam_Schemas
# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# model
from model.db_model import get_db
# crud
from crud.crud_setting import update_setting
from crud.crud_video import create_video , delete_video, delete_list_video,read_video, read_all_video

router = APIRouter(prefix="/video")

@router.post("/add")
async def add_Video(input: Video_Schemas, db: Session = Depends(get_db)):
    update_setting(input,db)
    result = process(input)
    record = create_video(result,db)
    return record

@router.delete("/delete")
async def delete_video_route(data: Delete_Video_Schemas,db: Session = Depends(get_db) ):
    return delete_video(data,db)

@router.delete("/delete_select")
async def delete_list_video_route(data: Delete_List_video_Schemas,db: Session = Depends(get_db) ):
    return delete_list_video(data,db)

@router.get("/get/{output_path}")
def get_video(output_path:str, db: Session = Depends(get_db)):
    return read_video(output_path,db)

@router.get("/get_all")
def get_all_video(db:Session = Depends(get_db)):
    return read_all_video(db)