from pydantic import BaseModel  # type: ignore
from datetime import date
from utils.calc import cal_now_date
# SQLite sẽ hiểu ngày tháng nếu bạn lưu dưới dạng chuỗi: YYYY-MM-DD.
class Create_User(BaseModel):
    name : str
    day_of_birth : date = None
    weight: float = 0
    height: int = 0
    email: str = None
    joined:date = cal_now_date()
    avatar: str = None
    total_session:  int = 0
    total_time_work :float = 0
    avg_accuracy :float = 0
    total_caloris :float = 0
    total_reps_count: int = 0
class Update_User(BaseModel):
    name: str = None
    joined: date = None
    weight: float = None
    height: int = None
    email: str = None
    day_of_birth: date = None

class Schemas_Update_detail(BaseModel):
    caloris: float
    average: float
    time_work: float
    reps: int