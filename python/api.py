from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel #type: ignore
from controller.controller import process, show_cam
# model
from model.delete_model import VideoDelete,ListVideoDelete
from model.webcam_model import webcam_model
from model.video_model import video_model

# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Boolean, Column, Float, ForeignKey,Integer, String, create_engine, JSON, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
SQLALCHEMY_DATABASE_URL = "sqlite:///../sql.poseApp.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///../sql.settingPoseApp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()
# ******************
class video(Base):
    __tablename__ = "video_result"
    id = Column(Integer,primary_key=True, index=True)
    output_path = Column(String)
    total = Column(Integer)
    count_good = Column(Integer)
    accuracy_good = Column(Float)
    type = Column(String)
    size_video = Column(String)
    form = Column(String)
    time = Column(String)
    # Sử dụng kiểu JSON để SQLAlchemy tự động convert dict/list Python cho bạn
    record_detail = Column(JSON)
    class Config:
            orm_mode = True 
class Setting(Base):
    __tablename__ = "setting_table"
    id = Column(Integer,primary_key=True, index=True)
    isDrawing = Column(String)
    isAnalyst = Column(String)
    isCheck_view = Column(String)
    Analyst_FPS = Column(String)
    Analyst_state = Column(String)
    Analyst_count = Column(String)
    Analyst_count_good = Column(String)
    Analyst_estimate = Column(String)

Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
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
async def add_Video(input: video_model, db: Session = Depends(get_db)):
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
async def delete_video(data: VideoDelete,db: Session = Depends(get_db) ):
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
async def delete_video(data: ListVideoDelete,db: Session = Depends(get_db) ):
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
def update_setting(input: video_model, db: Session = Depends(get_db)):
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
def show_webcam(input: webcam_model, db: Session = Depends(get_db)):
   show_cam(input)
