from sqlalchemy import Boolean, Column, Float, ForeignKey,Integer, String, create_engine, JSON, false
from model.db_model import Base
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