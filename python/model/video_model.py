from sqlalchemy import Boolean, Column, Float, ForeignKey,Integer, String, create_engine, JSON, false
from model.db_model import Base


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
    record_detail = Column(JSON)
    time_video = Column(String)
