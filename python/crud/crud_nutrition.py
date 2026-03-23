from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime, timedelta
from model.nutrition_model import (
    NutritionDay, FoodItem, MealLog, SleepRecord, ScheduleEntry
)
from schemas.nutrition_schemas import (
    FoodItemCreate, MealLogCreate, SleepRecordCreate,
    ScheduleEntryCreate, ScheduleEntryUpdate
)
from model.user_model import user

class CRUDNutrition:
    @staticmethod
    def get_all_food_items(db: Session):
        db = db.query(FoodItem).all()
        if not db:
            print("No food items found in database.")
        return db
    """CRUD operations for nutrition tracking"""
    @staticmethod
    def create_or_update_nutrition_day(db: Session, user_id: int, date_obj: date):
        from services.nutrition_service import AINutritionService

        db_user = db.query(user).filter(user.id == user_id).first()
        if not db_user:
            print(f"User with ID {user_id} not found when creating/updating nutrition day for date {date_obj}")
            return None
        nutrition_day = db.query(NutritionDay).filter(
            and_(NutritionDay.user_id == user_id, NutritionDay.date == date_obj)
        ).first()
        target_caloris = round(AINutritionService.calculate_daily_calories(db_user), 0)
        if not nutrition_day:
            nutrition_day = NutritionDay(
                user_id=user_id,
                date=date_obj,
                calories_target=target_caloris  # Default target
            )
            db.add(nutrition_day)
            db.commit()
        # print(f"Nutrition day record for user_id={user_id} on date={date_obj}: {nutrition_day.__dict__}")
        return nutrition_day
    
   # thay đổi nutriton của một ngày
    @staticmethod
    def add_meal(db: Session, user_id: int, meal_data: MealLogCreate):
        date_obj = meal_data.meal_time.date() if meal_data.meal_time else date.today()
        nutrition_day = CRUDNutrition.create_or_update_nutrition_day(db, user_id, date_obj)
        
        food = db.query(FoodItem).filter(FoodItem.id == meal_data.food_id).first()
        if not food:
            return None
        
        meal_log = MealLog(
            user_id=user_id,
            nutrition_day_id=nutrition_day.id,
            food_id=meal_data.food_id,
            servings=meal_data.servings,
            meal_time=meal_data.meal_time or datetime.now(),
            notes=meal_data.notes
        )
        # Update nutrition day totals
        nutrition_day.calories_consumed += (food.calories * meal_data.servings)
        nutrition_day.protein_grams += (food.protein * meal_data.servings)
        nutrition_day.carbs_grams += (food.carbs * meal_data.servings)
        nutrition_day.fat_grams += (food.fat * meal_data.servings)
        
        db.add(meal_log)
        db.commit()
        return meal_log
    
    @staticmethod
    def get_daily_nutrition(db: Session, user_id: int, date_obj: date):
        user_obj = db.query(user).filter(user.id == user_id).first()
        if not user_obj:
            print(f"User with ID {user_id} not found when fetching nutrition for date {date_obj}")
            return None
        
        nutrition_day = db.query(NutritionDay).filter(
            and_(NutritionDay.user_id == user_id, NutritionDay.date == date_obj)
        ).first()

        return nutrition_day
    @staticmethod
    def get_daily_meals(db: Session, user_id: int, date_obj: date):
        nutrition_day = CRUDNutrition.get_daily_nutrition(db, user_id, date_obj)
        if not nutrition_day:
            return []
        return db.query(MealLog).filter(MealLog.nutrition_day_id == nutrition_day.id).all()
    
    @staticmethod
    def add_food_item(db: Session, food_data: FoodItemCreate):
        food = FoodItem(**food_data.dict())
        db.add(food)
        db.commit()
        return food
    
    @staticmethod
    def get_foods_by_category(db: Session, category: str):
        return db.query(FoodItem).filter(FoodItem.category == category).all()
    
    @staticmethod
    def get_healthy_foods(db: Session, limit: int = 10):
        return db.query(FoodItem).filter(FoodItem.is_healthy == True).limit(limit).all()


class CRUDSleep:
    """CRUD operations for sleep tracking"""
    
    @staticmethod
    def create_sleep_record(db: Session, user_id: int, sleep_data: SleepRecordCreate):
        # Calculate sleep hours
        sleep_hours = CRUDSleep.calculate_sleep_hours(sleep_data.bedtime, sleep_data.wake_time)
        
        sleep_record = SleepRecord(
            user_id=user_id,
            date=sleep_data.date,
            bedtime=sleep_data.bedtime,
            wake_time=sleep_data.wake_time,
            sleep_hours=sleep_hours,
            sleep_quality=sleep_data.sleep_quality,
            notes=sleep_data.notes
        )
        
        db.add(sleep_record)
        db.commit()
        return sleep_record
    
    @staticmethod
    def calculate_sleep_hours(bedtime: str, wake_time: str) -> float:
        try:
            bed = datetime.strptime(bedtime, "%H:%M")
            wake = datetime.strptime(wake_time, "%H:%M")
            
            if wake < bed:
                wake += timedelta(days=1)
            
            duration = (wake - bed).total_seconds() / 3600
            return round(duration, 1)
        except:
            return 0
    
    @staticmethod
    def get_sleep_record(db: Session, user_id: int, date_obj: date):
        return db.query(SleepRecord).filter(
            and_(SleepRecord.user_id == user_id, SleepRecord.date == date_obj)
        ).first()
    
    @staticmethod
    def get_sleep_statistics(db: Session, user_id: int, days: int = 30):
        start_date = date.today() - timedelta(days=days)
        records = db.query(SleepRecord).filter(
            and_(
                SleepRecord.user_id == user_id,
                SleepRecord.date >= start_date
            )
        ).all()
        
        if not records:
            return None
        
        avg_sleep = sum(r.sleep_hours for r in records) / len(records)
        last_7_days = [r for r in records if r.date >= date.today() - timedelta(days=7)]
        last_7_avg = sum(r.sleep_hours for r in last_7_days) / len(last_7_days) if last_7_days else 0
        
        return {
            "total_records": len(records),
            "average_sleep": round(avg_sleep, 1),
            "last_7_days_avg": round(last_7_avg, 1),
            "consistency": calculate_consistency(records)
        }
    
    @staticmethod
    def get_recent_sleep(db: Session, user_id: int, days: int = 7):
        start_date = date.today() - timedelta(days=days)
        return db.query(SleepRecord).filter(
            and_(
                SleepRecord.user_id == user_id,
                SleepRecord.date >= start_date
            )
        ).order_by(SleepRecord.date.desc()).all()


class CRUDSchedule:
    """CRUD operations for schedule management"""
    
    @staticmethod
    def create_schedule_entry(db: Session, user_id: int, schedule_data: ScheduleEntryCreate):
        entry = ScheduleEntry(
            user_id=user_id,
            **schedule_data.dict()
        )
        db.add(entry)
        db.commit()
        return entry
    
    @staticmethod
    def update_schedule_entry(db: Session, entry_id: int, update_data: ScheduleEntryUpdate):
        entry = db.query(ScheduleEntry).filter(ScheduleEntry.id == entry_id).first()
        if entry:
            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(entry, key, value)
            db.commit()
        return entry
    
    @staticmethod
    def get_daily_schedule(db: Session, user_id: int, date_obj: date):
        return db.query(ScheduleEntry).filter(
            and_(ScheduleEntry.user_id == user_id, ScheduleEntry.date == date_obj)
        ).order_by(ScheduleEntry.time).all()
    
    @staticmethod
    def get_week_schedule(db: Session, user_id: int, start_date: date):
        end_date = start_date + timedelta(days=7)
        return db.query(ScheduleEntry).filter(
            and_(
                ScheduleEntry.user_id == user_id,
                ScheduleEntry.date >= start_date,
                ScheduleEntry.date < end_date
            )
        ).order_by(ScheduleEntry.date, ScheduleEntry.time).all()
    
    @staticmethod
    def mark_completed(db: Session, entry_id: int):
        entry = db.query(ScheduleEntry).filter(ScheduleEntry.id == entry_id).first()
        if entry:
            entry.status = "completed"
            db.commit()
        return entry
    
    @staticmethod
    def delete_schedule_entry(db: Session, entry_id: int):
        entry = db.query(ScheduleEntry).filter(ScheduleEntry.id == entry_id).first()
        if entry:
            db.delete(entry)
            db.commit()
            return True
        return False


def calculate_consistency(records: list) -> float:
    """Calculate schedule consistency (0-100%)"""
    if len(records) < 2:
        return 100
    
    times = [r.sleep_hours for r in records]
    avg = sum(times) / len(times)
    variance = sum((x - avg) ** 2 for x in times) / len(times)
    std_dev = variance ** 0.5
    
    # Higher std dev = less consistency
    consistency = max(0, 100 - (std_dev * 10))
    return round(consistency, 1)
