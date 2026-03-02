from pydantic import BaseModel
from datetime import date
class Create_User(BaseModel):
    name : str
    age : str = None
    weight: float = 0
    height: int = 0
    email: str = None
    day_of_birth: str = None
    total_session:  float = 0
    total_time_work :float = 0
    avg_accuracy :float = 0
    total_caloris :float = 0
    # tap luyen
class Update_User(BaseModel):
    name: str = None
    age: str = None
    weight: float = None
    height: int = None
    email: str = None
    day_of_birth: str = None