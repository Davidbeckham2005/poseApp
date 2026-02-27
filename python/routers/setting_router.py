from fastapi import FastAPI,APIRouter # type: ignore
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, relationship
from model.db_model import get_db,engine,Base
from crud.crud_setting import update_setting, read_setting

router = APIRouter(prefix="/setting")

@router.get("/get")
def get_setting(db: Session = Depends(get_db)):
   return read_setting(db)