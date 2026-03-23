from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

# ========== Nutrition Schemas ==========
class FoodItemBase(BaseModel):
    name: str
    serving_size: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = 0
    category: str
    is_healthy: Optional[bool] = True


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None


class FoodItemResponse(FoodItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# bữa ăn đã log với thông tin về thực phẩm, số lượng, thời gian ăn, và ghi chú
class MealLogCreate(BaseModel):
    food_id: int
    servings: float = 1
    meal_time: Optional[datetime] = None
    notes: Optional[str] = None


class MealLogResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    servings: float
    meal_time: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True

# dinh dưỡng tổng quan của một ngày cụ thể, bao gồm tổng calo, protein, carbs, fat đã tiêu thụ và các bữa ăn đã log trong ngày đó
class NutritionDayResponse(BaseModel):
    id: int
    date: date
    calories_consumed: float
    calories_burned: float
    calories_target: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    water_liters: float
    class Config:
        from_attributes = True


class NutritionSummaryResponse(BaseModel):
    date: date
    calories_consumed: float
    calories_burned: float
    calorie_deficit: float
    protein: float
    carbs: float
    fat: float
    water: float
    daily_goal: float
    meals: List[MealLogResponse] = []


# ========== Sleep Schemas ==========
class SleepRecordCreate(BaseModel):
    date: date
    bedtime: str
    wake_time: str
    sleep_quality: Optional[str] = "good"
    notes: Optional[str] = None


class SleepRecordUpdate(BaseModel):
    bedtime: Optional[str] = None
    wake_time: Optional[str] = None
    sleep_quality: Optional[str] = None
    notes: Optional[str] = None


class SleepRecordResponse(BaseModel):
    id: int
    user_id: int
    date: date
    bedtime: str
    wake_time: str
    sleep_hours: float
    sleep_quality: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SleepStatisticsResponse(BaseModel):
    total_nights: int
    average_sleep_hours: float
    average_quality: str
    last_7_days_avg: float
    sleep_schedule_consistency: float  # percentage


# ========== Schedule Schemas ==========
class ScheduleEntryCreate(BaseModel):
    date: date
    time: str
    activity: str
    duration: int
    activity_type: str
    description: Optional[str] = None
    reminder_enabled: Optional[bool] = True


class ScheduleEntryUpdate(BaseModel):
    time: Optional[str] = None
    activity: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None


class ScheduleEntryResponse(BaseModel):
    id: int
    user_id: int
    date: date
    time: str
    activity: str
    duration: int
    activity_type: str
    status: str
    description: Optional[str] = None
    reminder_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DailyScheduleResponse(BaseModel):
    date: date
    entries: List[ScheduleEntryResponse]


# ========== AI Nutrition Recommendation ==========
class NutritionRecommendationResponse(BaseModel):
    daily_calorie_goal: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    water_liters: float
    recommended_meals: List[FoodItemResponse] = []
    explanation: str


class AIMenuSuggestionResponse(BaseModel):
    breakfast: List[FoodItemResponse]
    lunch: List[FoodItemResponse]
    dinner: List[FoodItemResponse]
    snacks: List[FoodItemResponse]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
