from sqlalchemy import Boolean, Column, Date, Float, ForeignKey,Integer, String, column, create_engine, JSON, false   # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from model.db_model import Base
class user(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    day_of_birth = Column(Date)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Integer,default=0)
    email = Column(String)
    joined = Column(Date)
    BMI = Column(Float)
    type_BMI = Column(String)
    target_weight = Column(Float,default=0)
    avatar = Column(String)
    sex: String = Column(String, default="M")  
    activity_level = Column(String, default="moderate")  # Thêm trường activity_level để lưu mức độ hoạt động của người dùng
    goal = Column(String, default="maintain")  # Thêm trường goal để lưu mục tiêu thể dục của người dùng (giảm cân, tăng cơ, duy trì, cải thiện sức bền)

    total_reps_count = Column(Integer,default=0)
    total_session = Column(Integer,default=0)
    total_time_work = Column(Float,default=0)
    avg_accuracy = Column(Float,default=0)
    total_caloris = Column(Float,default=0)
    
    # ===== RELATIONSHIPS WITH NUTRITION PROFILE =====
    nutrition_days = relationship("NutritionDay", back_populates="user", cascade="all, delete-orphan")
    meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete-orphan")
    schedule_entries = relationship("ScheduleEntry", back_populates="user", cascade="all, delete-orphan")
    
