from pydantic import BaseModel  # type: ignore
from datetime import date, datetime
from typing import Optional, List
from utils.calc import cal_now_date

# SQLite sẽ hiểu ngày tháng nếu bạn lưu dưới dạng chuỗi: YYYY-MM-DD.
class Create_User(BaseModel):
    id: Optional[int] = None
    name: str
    day_of_birth: Optional[date] = None
    weight: float = 0
    height: int = 0
    email: Optional[str] = None
    joined: date = cal_now_date()
    avatar: Optional[str] = None
    target_caloris: float = 0
    target_weight: float = 0
    total_session: int = 0
    total_time_work: float = 0
    avg_accuracy: float = 0
    total_caloris: float = 0
    total_reps_count: float = 0
    age: Optional[int] = None
    BMI: Optional[float] = None
    type_BMI: Optional[str] = None
    sex: Optional[str] = "M"
    activity_level: Optional[str] = "moderate"  # Thêm trường activity_level để lưu mức độ hoạt động của người dùng
    goal: Optional[str] = "maintain"  # Thêm trường goal để lưu    
    class Config:
        from_attributes = True

class Update_User(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[int] = None
    email: Optional[str] = None
    day_of_birth: Optional[date] = None
    target_weight: Optional[float] = None
    sex: Optional[str] = None
    activity_level: Optional[str] = None
    class Config:
        from_attributes = True

class Schemas_Update_detail(BaseModel):
    caloris: float
    average: float
    time_work: float
    reps: float

    class Config:
        from_attributes = True


# ===== COMBINED USER + NUTRITION SCHEMAS =====
class DailyNutritionSummary(BaseModel):
    """Daily nutrition data linked to user"""
    id: int
    date: date
    calories_consumed: float
    calories_burned: float
    calories_target: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    water_liters: float
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileWithNutrition(BaseModel):
    """User profile combined with today's nutrition data"""
    # User basic info
    id: int
    name: str
    email: str
    weight: float
    height: int
    BMI: float
    type_BMI: str
    target_caloris: float  # Daily calorie target
    target_weight: float
    avatar: Optional[str]
    
    # Fitness metrics
    total_reps_count: int
    total_session: int
    total_time_work: float
    avg_accuracy: float
    total_caloris: float
    
    # Today's nutrition
    todays_nutrition: Optional[DailyNutritionSummary]
    
    class Config:
        from_attributes = True


class UserNutritionHistory(BaseModel):
    """User with last 7 days nutrition history"""
    # User info
    id: int
    name: str
    weight: float
    height: int
    target_caloris: float
    
    # Last 7 days nutrition
    nutrition_days: List[DailyNutritionSummary]
    
    class Config:
        from_attributes = True


# ===== RESPONSE WRAPPERS FOR ENDPOINTS =====
class UserWithNutritionResponse(BaseModel):
    """Wrapper for user + today's nutrition API response"""
    user: Create_User
    todays_nutrition: Optional[DailyNutritionSummary] = None
    
    class Config:
        from_attributes = True


class UserWithNutritionHistoryResponse(BaseModel):
    """Wrapper for user + nutrition history API response"""
    user: Create_User
    nutrition_days: List[DailyNutritionSummary]
    
    class Config:
        from_attributes = True