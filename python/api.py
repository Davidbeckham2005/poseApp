from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from controller.controller import process, show_cam
# schemas
from schemas.video_schemas import Delete_Video_Schemas, Delete_List_video_Schemas, Video_Schemas, Webcam_Schemas

# model
from model import db_model
from model.db_model import get_db,engine,Base
# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, relationship
from model.video_model import video
from model.setting_model import Setting

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
    new_video = video(
    output_path = result["result"]["src_output"],
    total = result["result"]["total"],
    count_good = result["result"]["good"],
    accuracy_good = result["result"]["accuracy"],
    record_detail = result["result"]["record"],
    type = result['type'],
    size_video = result['result']['size'],
    form = result['result']['form'],
    time = result['result']['time']
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

@app.delete("/deleteVideo/")
async def delete_video(data: Delete_Video_Schemas,db: Session = Depends(get_db) ):
    video_to_delete = db.query(video).filter(video.output_path == data.output_path).first()
    if not video_to_delete:
        raise HTTPException(status_code=404, detail="Video không tồn tại")
    try:
        db.delete(video_to_delete)
        db.commit()
    except Exception as e:
        db.rollback() # Hoàn tác nếu có lỗi xảy ra
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa: {str(e)}")
# de;ete list video

@app.delete("/deleteVideos/")
async def delete_video(data: Delete_List_video_Schemas,db: Session = Depends(get_db) ):
    videos = db.query(video).filter(video.output_path.in_(data.output_paths))
    count = videos.count()
    if count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy video nào")
    try:
        videos.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback() # Hoàn tác nếu có lỗi xảy ra
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa: {str(e)}")
def update_setting(input: Video_Schemas, db: Session = Depends(get_db)):
    db_setting =  db.query(Setting).filter(Setting.id == 1).first()
    if db_setting:
        db_setting.isDrawing = input.isDrawing
        db_setting.isAnalyst = input.isAnalyst
        db_setting.isCheck_view = input.isCheck_view
        db_setting.Analyst_FPS = input.Analyst_FPS
        db_setting.Analyst_state = input.Analyst_state
        db_setting.Analyst_count = input.Analyst_count
        db_setting.Analyst_count_good = input.Analyst_count_good
        db_setting.Analyst_estimate = input.Analyst_estimate
    else:
        new_setting = Setting(
            id=1,
            isDrawing = input.isDrawing,
            Analyst_FPS = input.Analyst_FPS,
            Analyst_state = input.Analyst_state,
            isAnalyst = input.isAnalyst,
            isCheck_view = input.isCheck_view,
            Analyst_count = input.Analyst_count,
            Analyst_count_good = input.Analyst_count_good,
            Analyst_estimate = input.Analyst_estimate,
        )
        db.add(new_setting)
    db.commit()

@app.get("/get_setting")
def get_setting(db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.id == 1).first()
    return setting
@app.get("/get_video/{filename}")
def get_video_content(filename:str, db: Session = Depends(get_db)):
    video_content = db.query(video).filter(video.output_path==filename).first()

    if video_content:
         return video_content
    return {"message":"Khong tim thay"}

@app.get("/get_video/")
def get_all_video(db:Session = Depends(get_db)):
    videos = db.query(video).all()
    total_video = len(videos)
    return {
         "total" : total_video,
         "video_items" : videos
    }

@app.post("/show_webcam/")
def show_webcam(input: Webcam_Schemas, db: Session = Depends(get_db)):
   show_cam(input)
