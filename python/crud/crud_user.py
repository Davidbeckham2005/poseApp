from model.db_model import get_db
from sqlalchemy.orm import Session
from fastapi import  Depends
from model.user_model import user
from utils.calc import calculating_BMI, detect_type_BMI
def create(data, db: Session = Depends(get_db)):
    new_user = user(
        name = data.name,
        day_of_birth = data.day_of_birth,
        height = data.height,
        weight = data.weight,
        email= data.email,
        total_session = data.total_session,
        total_time_work  = data.total_time_work,
        avg_accuracy  = data.avg_accuracy,
        total_caloris  = data.total_caloris,
        total_reps_count = data.total_reps_count,
        BMI = calculating_BMI(data.weight, data.height),
        type_BMI = detect_type_BMI(calculating_BMI(data.weight, data.height))
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(db: Session = Depends(get_db)):
    user_to_get = db.query(user).filter(user.id == 1).first()
    return {
        "user" :user_to_get
    }

def update(data, db: Session = Depends(get_db)) :
    # 1. Tìm user trong database
    db_user = db.query(user).filter(user.id == 1).first()
    
    if not db_user:
        print("Không tìm thấy user với ID = 1")
        return None

    # 2. Lấy dữ liệu dưới dạng Dict, chỉ lấy các trường người dùng gửi lên
    update_data = data.dict(exclude_unset=True)
    
    # 3. Cập nhật các trường cơ bản một cách linh hoạt
    for key, value in update_data.items():
        setattr(db_user, key, value)

    # 4. Tính toán lại BMI nếu có thay đổi về cân nặng hoặc chiều cao
    # Chúng ta lấy giá trị từ db_user để đảm bảo có đủ dữ liệu cũ + mới
    if db_user.weight and db_user.height and db_user.height > 0:
        new_bmi = calculating_BMI(db_user.weight, db_user.height)
        db_user.BMI = new_bmi
        db_user.type_BMI = detect_type_BMI(new_bmi)
    db.commit()
    db.refresh(db_user)
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