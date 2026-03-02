from sqlalchemy import Boolean, Column, Date, Float, ForeignKey,Integer, String, column, create_engine, JSON, false
from model.db_model import Base
class user(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    day_of_birth = Column(String)
    weight = Column(Float)
    height = Column(Integer)
    email = Column(String)
    
    BMI = column(float)
    type_BMI = Column(String)
    # tap luyen
    total_reps_count = Column(Integer)
    total_session = Column(Integer)
    total_time_work = Column(Float)
    avg_accuracy = Column(Float)
    total_caloris = Column(Float)
    
