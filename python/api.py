from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel #type: ignore
from controller.controller import process

# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Float, ForeignKey,Integer, String, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

class data_Video(BaseModel):
    isDrawing: bool = True
    isAnalyst: bool = True
    isCheck_view: bool = True
    type: str
    path_video: str
# **********
SQLALCHEMY_DATABASE_URL = "sqlite:///../../sql.poseApp.db"
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
    # Sử dụng kiểu JSON để SQLAlchemy tự động convert dict/list Python cho bạn
    record_detail = Column(JSON)
    class Config:
            orm_mode = True 
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
async def add_Video(input: data_Video, db: Session = Depends(get_db)):
    result = process(input)
    new_video = video(
    output_path = result["result"]["src_output"],
    total = result["result"]["total"],
    count_good = result["result"]["good"],
    accuracy_good = result["result"]["accuracy"],
    record_detail = result["result"]["record"],
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

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