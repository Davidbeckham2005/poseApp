from fastapi import APIRouter # type: ignore
# schemas
from schemas.user_schemas import (
    Create_User, Update_User, Schemas_Update_detail,
    UserProfileWithNutrition, UserNutritionHistory,
    UserWithNutritionResponse, UserWithNutritionHistoryResponse
)
# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
# model
from model.db_model import get_db
# crud
from crud.crud_user import (
    create, get, update, update_detail,
    get_user_with_today_nutrition, get_user_nutrition_history,
    link_user_target_to_nutrition
)

router = APIRouter(prefix="/user")
@router.post("/create", response_model=Create_User)
def add_user(data: Create_User,db: Session = Depends(get_db)):
    return create(data,db)

@router.get("/get", response_model=Create_User)
def get_user(db: Session = Depends(get_db)):
    return get(db)

@router.post("/update", response_model=Create_User)
def update_user(data :Update_User, db: Session = Depends(get_db)):
    return update(data, db)

@router.post("/update_detail", response_model=Create_User)
def route_update_detail(data: Schemas_Update_detail, db: Session = Depends(get_db)):
    return update_detail(data,db)


# ===== ENDPOINTS FOR LINKED USER + NUTRITION =====
@router.get("/{user_id}/profile-with-nutrition", response_model=UserWithNutritionResponse)
def get_user_profile_with_nutrition(user_id: int, db: Session = Depends(get_db)):
    """Get user profile combined with today's nutrition data"""
    result = get_user_with_today_nutrition(user_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/{user_id}/nutrition-history", response_model=UserWithNutritionHistoryResponse)
def get_user_nutrition_history_endpoint(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    """Get user with last N days nutrition history"""
    result = get_user_nutrition_history(user_id, days, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/{user_id}/sync-nutrition-target")
def sync_user_nutrition_target(user_id: int, db: Session = Depends(get_db)):
    """
    Synchronize user's daily calorie target to today's nutrition record.
    Call this after updating user's target_caloris.
    """
    result = link_user_target_to_nutrition(user_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Nutrition target synced", "user": result}