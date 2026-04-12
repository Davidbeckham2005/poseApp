from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List

from model.db_model import get_db
from model.user_model import user
from schemas.nutrition_schemas import (
    FoodItemCreate, FoodItemResponse, MealLogCreate, MealLogResponse,
    NutritionDayResponse, NutritionSummaryResponse, SleepRecordCreate,
    SleepRecordResponse, SleepStatisticsResponse, ScheduleEntryCreate,
    ScheduleEntryResponse, DailyScheduleResponse, NutritionRecommendationResponse,
    AIMenuSuggestionResponse, ScheduleEntryUpdate, CalorieBurnSummaryResponse
)
from crud.crud_nutrition import CRUDNutrition, CRUDSleep, CRUDSchedule
from services.nutrition_service import AINutritionService

router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])


# ========== Food Management Routes ==========
# thêm thực phẩm mới vào database với thông tin dinh dưỡng
@router.post("/foods", response_model=FoodItemResponse)
def create_food_item(food: FoodItemCreate, db: Session = Depends(get_db)):
    """Add a new food item to database"""
    return CRUDNutrition.add_food_item(db, food)

# lấy danh sách thực phẩm theo category
@router.get("/foods/category/{category}", response_model=List[FoodItemResponse])
def get_foods_by_category(category: str, db: Session = Depends(get_db)):
    """Get all foods in a specific category"""
    return CRUDNutrition.get_foods_by_category(db, category)

# lấy danh sách thực phẩm healthy
@router.get("/foods/healthy", response_model=List[FoodItemResponse])
def get_healthy_foods(limit: int = 10, db: Session = Depends(get_db)):
    """Get recommended healthy foods"""
    return CRUDNutrition.get_healthy_foods(db, limit)

# lấy tất cả thực phẩm trong database, được sử dụng để hiển thị trong giao diện người dùng khi log bữa ăn hoặc tạo kế hoạch bữa ăn
@router.get("/foods/get_all", response_model=List[FoodItemResponse])
def get_all_food_items(db: Session = Depends(get_db)):
    """Get all food items in the database"""
    return CRUDNutrition.get_all_food_items(db)
# ========== Meal Logging Routes ==========
# người dùng log một bữa ăn với thông tin về thực phẩm, số lượng, thời gian ăn, và ghi chú
@router.post("/user/{user_id}/meals", response_model=MealLogResponse)
def log_meal(user_id: int, meal: MealLogCreate, db: Session = Depends(get_db)):
    """Log a meal for user"""
    result = CRUDNutrition.add_meal(db, user_id, meal)
    if not result:
        raise HTTPException(status_code=404, detail="Food item not found")
    return result
@router.post("/user/{user_id}/nutrition/calories_burned", response_model=NutritionDayResponse)
def update_todays_nutrition(user_id: int,calories_burn: CalorieBurnSummaryResponse, db: Session = Depends(get_db)):
    if calories_burn.calories_burned < 0:
        raise HTTPException(status_code=400, detail="calories_burned must be >= 0")

    target_date = calories_burn.date or date.today()
    nutrition = CRUDNutrition.add_calories_burned(db, user_id, target_date, calories_burn)
    if not nutrition:
        raise HTTPException(status_code=404, detail="User not found or unable to create nutrition day")
    return nutrition
@router.get("/user/{user_id}/nutrition/all")
def get_nutrition_range(user_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)):
    """Get nutrition summary for a date range"""
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    if start_date_obj > end_date_obj:
        raise HTTPException(status_code=400, detail="start_date must be before or equal to end_date.")
    
    return CRUDNutrition.get_nutrition_range(db, user_id, start_date_obj, end_date_obj)
# lấy thông tin dinh dưỡng tổng quan của một ngày cụ thể, bao gồm tổng calo, protein, carbs, fat đã tiêu thụ và các bữa ăn đã log trong ngày đó
# nếu
@router.get("/user/{user_id}/nutrition/{date_str}", response_model=NutritionDayResponse)
def get_daily_nutrition(user_id: int,date_str: str,db: Session = Depends(get_db)):
    """Get daily nutrition summary"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(f"Fetching nutrition for user_id={user_id} on date={date_obj}")
    nutrition = CRUDNutrition.create_or_update_nutrition_day(db, user_id, date_obj)
    
    if not nutrition:
        raise HTTPException(status_code=404, detail="No nutrition data for this date")
    print(f"Nutrition data for user_id={user_id} on date={date_obj}: {nutrition}")
    return nutrition

# lấy tất cả bữa ăn đã log cho một ngày cụ thể
@router.get("/user/{user_id}/meals/{date_str}", response_model=List[MealLogResponse])
def get_daily_meals(
    user_id: int,
    date_str: str,
    db: Session = Depends(get_db)
):
    """Get all meals logged for a specific date"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    return CRUDNutrition.get_daily_meals(db, user_id, date_obj)


# ========== AI Nutrition Recommendations ==========
@router.get("/recommend/{user_id}", response_model=NutritionRecommendationResponse)
def get_nutrition_recommendation(user_id: int,activity_level: str = "moderate",db: Session = Depends(get_db)):
    """Get personalized AI nutrition recommendation"""
    user_obj = db.query(user).filter(user.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    return AINutritionService.get_nutrition_recommendation(
        db, user_obj, user_id, activity_level
    )

# hàm lấy gợi ý thực đơn hàng ngày được tạo bởi AI dựa trên nhu cầu calo mục tiêu của người dùng và mục tiêu thể dục của họ, đảm bảo lựa chọn thực phẩm phù hợp với mục tiêu và sở thích của người dùng
@router.get("/menu/{user_id}", response_model=AIMenuSuggestionResponse)
def get_daily_menu_suggestion(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get AI-generated daily menu suggestion"""
    user_obj = db.query(user).filter(user.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    daily_calories = AINutritionService.calculate_daily_calories(user_obj)
   
    return AINutritionService.generate_daily_menu(db, daily_calories)


# ========== Sleep Tracking Routes ==========
@router.post("/sleep/{user_id}", response_model=SleepRecordResponse)
def log_sleep(
    user_id: int,
    sleep_data: SleepRecordCreate,
    db: Session = Depends(get_db)
):
    """Log sleep for a user"""
    return CRUDSleep.create_sleep_record(db, user_id, sleep_data)


@router.get("/sleep/{user_id}/{date_str}", response_model=SleepRecordResponse)
def get_sleep_record(
    user_id: int,
    date_str: str,
    db: Session = Depends(get_db)
):
    """Get sleep record for a specific date"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    sleep = CRUDSleep.get_sleep_record(db, user_id, date_obj)
    
    if not sleep:
        raise HTTPException(status_code=404, detail="No sleep record for this date")
    return sleep


@router.get("/sleep/stats/{user_id}", response_model=dict)
def get_sleep_statistics(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get sleep statistics"""
    stats = CRUDSleep.get_sleep_statistics(db, user_id, days)
    if not stats:
        raise HTTPException(status_code=404, detail="No sleep data found")
    return stats


@router.get("/sleep/recommendation/{user_id}")
def get_sleep_recommendation(user_id: int, db: Session = Depends(get_db)):
    """Get personalized sleep recommendations"""
    return AINutritionService.get_sleep_recommendation(db, user_id)


@router.get("/sleep/recent/{user_id}", response_model=List[SleepRecordResponse])
def get_recent_sleep(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    """Get recent sleep records"""
    return CRUDSleep.get_recent_sleep(db, user_id, days)


# ========== Schedule Management Routes ==========
@router.post("/schedule/{user_id}", response_model=ScheduleEntryResponse)
def create_schedule_entry(
    user_id: int,
    entry: ScheduleEntryCreate,
    db: Session = Depends(get_db)
):
    """Create a schedule entry"""
    return CRUDSchedule.create_schedule_entry(db, user_id, entry)


@router.put("/schedule/{entry_id}", response_model=ScheduleEntryResponse)
def update_schedule_entry(
    entry_id: int,
    update_data: ScheduleEntryUpdate,
    db: Session = Depends(get_db)
):
    """Update a schedule entry"""
    entry = CRUDSchedule.update_schedule_entry(db, entry_id, update_data)
    if not entry:
        raise HTTPException(status_code=404, detail="Schedule entry not found")
    return entry


@router.get("/schedule/{user_id}/{date_str}", response_model=DailyScheduleResponse)
def get_daily_schedule(
    user_id: int,
    date_str: str,
    db: Session = Depends(get_db)
):
    """Get schedule for a specific date"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    entries = CRUDSchedule.get_daily_schedule(db, user_id, date_obj)
    
    return DailyScheduleResponse(date=date_obj, entries=entries)


@router.get("/schedule/week/{user_id}/{start_date_str}")
def get_week_schedule(
    user_id: int,
    start_date_str: str,
    db: Session = Depends(get_db)
):
    """Get schedule for a week"""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    entries = CRUDSchedule.get_week_schedule(db, user_id, start_date)
    return entries


@router.patch("/schedule/{entry_id}/complete")
def mark_schedule_complete(entry_id: int, db: Session = Depends(get_db)):
    """Mark schedule entry as completed"""
    entry = CRUDSchedule.mark_completed(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Schedule entry not found")
    return {"status": "completed", "entry": entry}


@router.delete("/schedule/{entry_id}")
def delete_schedule_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete a schedule entry"""
    if not CRUDSchedule.delete_schedule_entry(db, entry_id):
        raise HTTPException(status_code=404, detail="Schedule entry not found")
    return {"message": "Schedule entry deleted"}


@router.get("/schedule/{user_id}/today")
def get_todays_schedule(user_id: int, db: Session = Depends(get_db)):
    """Get today's schedule"""
    return CRUDSchedule.get_daily_schedule(db, user_id, date.today())
