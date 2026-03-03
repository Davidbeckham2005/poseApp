from sqlalchemy import Boolean, Column, Date, Float, ForeignKey,Integer, String, column, create_engine, JSON, false   # type: ignore
from model.db_model import Base
class user(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    day_of_birth = Column(Date)
    weight = Column(Float)
    height = Column(Integer,default=0)
    email = Column(String)
    joined = Column(Date)
    BMI = Column(Float)
    type_BMI = Column(String)
    avatar = Column(String)
    # tap luyen
    total_reps_count = Column(Integer,default=0)
    total_session = Column(Integer,default=0)
    total_time_work = Column(Float,default=0)
    avg_accuracy = Column(Float,default=0)
    total_caloris = Column(Float,default=0)
    
