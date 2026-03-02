from fastapi import APIRouter # type: ignore
# schemas
from schemas.user_schemas import Create_User, Update_User
# cau hinh sqlite
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# model
from model.db_model import get_db
# crud
from crud.crud_user import create, get, update

router = APIRouter(prefix="/user")
@router.post("/add")
def add_user(data: Create_User,db: Session = Depends(get_db)):
    return create(data,db)

@router.get("/get")
def get_user(db: Session = Depends(get_db)):
    return get(db)

@router.post("/update")
def update_user(data: Update_User, db: Session = Depends(get_db)):
    return update(data,db)