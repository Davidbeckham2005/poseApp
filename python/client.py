# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import Column, ForeignKey,Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session, relationship
# from pydantic import BaseModel
# # cau hinh sqlite

# class UserUpdate(BaseModel):
#     new_name: str
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql.app.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer,primary_key=True, index=True)
#     name = Column(String)
#     accounts = relationship("Account",back_populates="owner")
# class Account(Base):
#     __tablename__ = "account"
#     id = Column(Integer,primary_key=True, index=True)
#     username = Column(String)
#     owner_user_id = Column(Integer, ForeignKey("users.id"))
#     # giup minh ket noi nguoc lai voi bang user
#     # Ở đây, SQLAlchemy không nhìn xuống Database. Nó đang nhìn vào các file Python của bạn.

# # Nó đi tìm xem có cái Class nào tên là User hay không để nó kết nối các thuộc tính (như .name, .id) vào biến owner.
#     owner = relationship("User", back_populates="accounts")

# Base.metadata.create_all(bind=engine)

# # tao app
# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/create_user/{name}")
# def create_user(name:str, db: Session = Depends(get_db)):
#     new_user = User(name=name)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": f"Đã tạo user{name}"}
    
# @app.get("/user")
# def get_all_user(db: Session = Depends(get_db)):
#     return db.query(User).all()

# @app.get("/user/{id}")
# def get_user(id:int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == id).first()
#     if user:
#         return user
#     return {"msg": "Khong tim thay user!"}
# @app.delete("/delete-user/{user_id}")
# def delete_user(user_id:int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user:
#         db.delete(user)
#         db.commit()
#         return {"msg": "Done!"}
#     return {"msg":"Ko tim thay"}

# @app.put("/update_user/{user_id}")
# def update_user(user_id:int, uservalue: UserUpdate, db:Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="Not found")
    

#     user.name = uservalue.new_name
#     db.commit()
#     db.refresh(user)

#     return {"msg":"Cập nhật thành công user"}


# @app.post("/account/create/{username}")
# def create_account(username:str,db:Session = Depends(get_db)):
#     new_account = Account(username=username)
#     db.add(new_account)
#     db.commit()
#     db.refresh(new_account)
#     return {"msg" : f"tao account thanh cong!{username}"}
# @app.get("/account/get")
# def get_all_account(db:Session = Depends(get_db)):
#     accounts = db.query(Account).all()
#     return accounts
# # Tạo 1 account thuộc về user
# @app.post("/create_account/{user_id}")
# def create_account_for_user(user_id: int, username:str, db:Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.id==user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="Not found")
#     new_account = Account(username=username, owner_user_id= user_id )
    
#     db.add(new_account)
#     db.commit()
#     # giong nhu f5 du lieu
#     db.refresh(new_account)

#     return {
#         "msg" : "tao thanh cong"
#     }

# # tim tat ca account cua user 

# @app.get("/get_all_account_user")
# def get_all_count_of_user(id:int, db:Session = Depends(get_db)):
#     # user = db.query(User).filter(User.id==id).first()
#     # if not user:
#     #     HTTPException(status_code=404, detail="Not Found!")
#     accounts = db.query(Account).filter(Account.owner_user_id==id).all()
#     if not accounts:
#         raise HTTPException(status_code=404, detail="Not Found!")
#     return accounts

