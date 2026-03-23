from datetime import date, timedelta
import logging
from schemas.user_schemas import Create_User as UserSchema, DailyNutritionSummary
from datetime import datetime
from model.db_model import get_db
from sqlalchemy.orm import Session # type: ignore
from fastapi import  Depends # type: ignore
from model.user_model import user
from model.nutrition_model import NutritionDay
from utils.calc import calculating_BMI, detect_goal, detect_type_BMI, cal_age, get_now
from services.nutrition_service import AINutritionService
from crud.crud_nutrition import CRUDNutrition
logging.basicConfig(level=logging.INFO)
def create(data, db: Session = Depends(get_db)):
    new_user = user(
        name = data.name,
        day_of_birth = data.day_of_birth,
        joined = data.joined,
        height = data.height,
        weight = data.weight,
        email= data.email,
        target_weight = data.target_weight,
        total_session = data.total_session,
        total_time_work  = data.total_time_work,
        avg_accuracy  = data.avg_accuracy,
        age = cal_age(data.day_of_birth) if data.day_of_birth else None,
        total_caloris  = data.total_caloris,
        total_reps_count = data.total_reps_count,
        avatar = data.avatar,
        BMI = calculating_BMI(data.weight, data.height),
        type_BMI = detect_type_BMI(calculating_BMI(data.weight, data.height)),
        goal = detect_goal(data),
        activity_level = data.activity_level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    link_user_target_to_nutrition(new_user.id, db)
    return new_user

def get(db: Session = Depends(get_db)):
    user_to_get = db.query(user).filter(user.id == 1).first()
    logging.info(f"Lấy thông tin user_id=1 vào lúc ")
    logging.info(f"Thông tin user: {user_to_get.__dict__ }")
    return user_to_get

# Cập nhật thông tin cơ bản của user, có thể cập nhật một số trường hoặc tất cả
def update(data, db: Session = Depends(get_db)) :
    db_user = db.query(user).filter(user.id == 1).first()
    if not db_user:
        print("Không tìm thấy user với ID = 1")
        return None
    update_data = data.dict(exclude_unset=True)
    print(f"Dữ liệu cập nhật nhận được: {update_data} vào lúc {date.today()}")
    # 3. Cập nhật các trường cơ bản một cách linh hoạt
    for key, value in update_data.items():
        setattr(db_user, key, value)
    if "day_of_birth" in update_data:
        db_user.age = cal_age(update_data["day_of_birth"])
    if "weight" in update_data or "target_weight" in update_data:
        db_user.goal = detect_goal(db_user)
    # 4. Tính toán lại BMI nếu có thay đổi về cân nặng hoặc chiều cao
    # Chúng ta lấy giá trị từ db_user để đảm bảo có đủ dữ liệu cũ + mới
    if db_user.weight and db_user.height and db_user.height > 0:
        new_bmi = calculating_BMI(db_user.weight, db_user.height)
        db_user.BMI = new_bmi
        db_user.type_BMI = detect_type_BMI(new_bmi)
    target_caloris = round(AINutritionService.calculate_daily_calories(db_user), 0)
    nutrition_day = CRUDNutrition.create_or_update_nutrition_day(db, db_user.id, date.today())
    if nutrition_day:
        nutrition_day.calories_target = target_caloris
    
    
    db.commit()
    db.refresh(db_user)

    print(f"Thông tin user sau khi cập nhật: {db_user.__dict__} vào lúc {get_now()}")
    return db_user

def update_detail(data, db: Session = Depends(get_db)):
    db_user =  db.query(user).filter(user.id == 1).first()
    if not db_user:
        print("Không tìm thấy user với ID = 1")
        return None
    
    new_caloris = db_user.total_caloris + data.caloris
    new_session = db_user.total_session + 1
    new_average = (db_user.avg_accuracy * db_user.total_session + data.average)/(new_session)
    new_time_work = db_user.total_time_work*60 + data.caloris
    new_reps_count = db_user.total_reps_count + data.reps
    db_user.total_caloris = round(new_caloris,0)
    db_user.total_session = new_session
    db_user.avg_accuracy = round(new_average,1)
    db_user.total_time_work = round(new_time_work/60,2)
    db_user.total_reps_count = new_reps_count
    try:
        db.commit()      
        db.refresh(db_user) 
        return db_user
    except Exception as e:
        db.rollback()   
        print(f"Lỗi khi update: {e}")
        return None


# ===== COMBINED USER + NUTRITION OPERATIONS =====
def get_user_with_today_nutrition(user_id: int, db: Session):
    db_user = db.query(user).filter(user.id == user_id).first()
    if not db_user:
        return None
    
    # Convert ORM object to Pydantic model
    user_data = UserSchema.from_orm(db_user)
    
    # Get today's nutrition data
    today_nutrition = db.query(NutritionDay).filter(
        (NutritionDay.user_id == user_id) & 
        (NutritionDay.date == date.today())
    ).first()
    
    nutrition_data = None
    if today_nutrition:
        nutrition_data = DailyNutritionSummary.from_orm(today_nutrition)
    
    return {
        "user": user_data,
        "todays_nutrition": nutrition_data
    }


def get_user_nutrition_history(user_id: int, days: int = 7, db: Session = None):
    """Get user with last N days nutrition history - returns Pydantic models"""
    from schemas.user_schemas import Create_User as UserSchema, DailyNutritionSummary
    
    if db is None:
        from model.db_model import SessionLocal
        db = SessionLocal()
    
    db_user = db.query(user).filter(user.id == user_id).first()
    if not db_user:
        return None
    
    # Convert ORM object to Pydantic model
    user_data = UserSchema.from_orm(db_user)
    
    # Get last N days nutrition
    start_date = date.today() - timedelta(days=days)
    nutrition_history = db.query(NutritionDay).filter(
        (NutritionDay.user_id == user_id) & 
        (NutritionDay.date >= start_date)
    ).order_by(NutritionDay.date.desc()).all()
    
    # Convert ORM objects to Pydantic models
    nutrition_data = [DailyNutritionSummary.from_orm(nh) for nh in nutrition_history]
    
    return {
        "user": user_data,
        "nutrition_days": nutrition_data
    }

def link_user_target_to_nutrition(user_id: int, db: Session):
    """
    Synchronize user's target_caloris to today's NutritionDay
    Useful after updating user's daily calorie target
    """
    
    db_user = db.query(user).filter(user.id == user_id).first()
    if not db_user:
        return None
    
    nutrition_day = db.query(NutritionDay).filter(
        (NutritionDay.user_id == user_id) & 
        (NutritionDay.date == date.today())
    ).first()
    target_calories = round(AINutritionService.calculate_daily_calories(db_user), 0)
    
    if not nutrition_day:
        nutrion = NutritionDay(
            user_id=user_id,
            date= date.today(),
            calories_consumed=0,
            calories_burned=0,
            calories_target= target_calories,
            protein_grams=0,
            carbs_grams=0,
            fat_grams=0
        )
        db.add(nutrion)
        db.commit()
    return db_user, nutrition_day