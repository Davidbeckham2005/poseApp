from controller.controller import process, show_cam
from model.db_model import get_db
from sqlalchemy.orm import Session
from fastapi import  Depends
from model.setting_model import Setting

def read_setting(db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.id == 1).first()
    return setting

def update_setting(input, db: Session = Depends(get_db)):
    db_setting =  db.query(Setting).filter(Setting.id == 1).first()
    if db_setting:
        db_setting.isDrawing = input.isDrawing
        db_setting.isAnalyst = input.isAnalyst
        db_setting.isCheck_view = input.isCheck_view
        db_setting.Analyst_FPS = input.Analyst_FPS
        db_setting.Analyst_state = input.Analyst_state
        db_setting.Analyst_count = input.Analyst_count
        db_setting.Analyst_count_good = input.Analyst_count_good
        db_setting.Analyst_estimate = input.Analyst_estimate
    else:
        new_setting = Setting(
            id=1,
            isDrawing = input.isDrawing,
            Analyst_FPS = input.Analyst_FPS,
            Analyst_state = input.Analyst_state,
            isAnalyst = input.isAnalyst,
            isCheck_view = input.isCheck_view,
            Analyst_count = input.Analyst_count,
            Analyst_count_good = input.Analyst_count_good,
            Analyst_estimate = input.Analyst_estimate,
        )
        db.add(new_setting)
    db.commit()
