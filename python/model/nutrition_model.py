from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship  # type: ignore
from datetime import datetime
from model.db_model import Base
from model.user_model import user
class NutritionDay(Base):
    """Track daily nutrition intake"""
    __tablename__ = "nutrition_day"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    date = Column(Date, index=True)
    calories_consumed = Column(Float, default=0)
    calories_burned = Column(Float, default=0)
    calories_target = Column(Float, default=2000)
    protein_grams = Column(Float, default=0)
    carbs_grams = Column(Float, default=0)
    fat_grams = Column(Float, default=0)
    water_liters = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    # nutrition_day liên kết với user thông qua user_id, và có thể có nhiều meal_logs
    user = relationship("user", back_populates="nutrition_days")
    meal_logs = relationship("MealLog", back_populates="nutrition_day", cascade="all, delete-orphan")


class FoodItem(Base):
    """Food database with nutrition info"""
    __tablename__ = "food_item"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    serving_size = Column(String)  # e.g., "100g", "1 cup"
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float, default=0)
    category = Column(String)  # breakfast, lunch, dinner, snack, etc.
    is_healthy = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MealLog(Base):
    """User's meal entries"""
    __tablename__ = "meal_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    nutrition_day_id = Column(Integer, ForeignKey("nutrition_day.id"), index=True)
    food_id = Column(Integer, ForeignKey("food_item.id"), index=True)
    servings = Column(Float, default=1)
    meal_time = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    user = relationship("user", back_populates="meal_logs")
    nutrition_day = relationship("NutritionDay", back_populates="meal_logs")
    food = relationship("FoodItem")


class SleepRecord(Base):
    """Sleep tracking"""
    __tablename__ = "sleep_record"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    date = Column(Date, index=True)
    bedtime = Column(String)  # HH:MM format
    wake_time = Column(String)  # HH:MM format
    sleep_hours = Column(Float)
    sleep_quality = Column(String)  # poor, fair, good, excellent
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("user", back_populates="sleep_records")


class ScheduleEntry(Base):
    """Schedule for workouts and wellness"""
    __tablename__ = "schedule_entry"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    date = Column(Date, index=True)
    time = Column(String)  # HH:MM format
    activity = Column(String)  # exercise type, meal time, etc.
    duration = Column(Integer)  # minutes
    activity_type = Column(String)  # workout, meal, rest, etc.
    description = Column(String, nullable=True)
    reminder_enabled = Column(Boolean, default=True)
    status = Column(String, default="pending")  # pending, completed, skipped
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("user", back_populates="schedule_entries")
