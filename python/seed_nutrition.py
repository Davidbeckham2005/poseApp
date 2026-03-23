"""
Seed database with initial food items for nutrition tracking
Run once to populate food database
"""
from sqlalchemy.orm import Session
from model.db_model import SessionLocal, engine, Base
from model.nutrition_model import FoodItem
from crud.crud_nutrition import CRUDNutrition
from schemas.nutrition_schemas import FoodItemCreate


def seed_food_database():
    """Populate database with common food items"""
    
    db = SessionLocal()
    
    # Check if foods already exist
    existing = db.query(FoodItem).first()
    if existing:
        print("Database already seeded!")
        return
    
    foods_data = [
    # Bữa sáng
    FoodItemCreate(name="Yến mạch với quả mọng", serving_size="1 cốc", calories=200, protein=6, carbs=35, fat=4, fiber=5, category="breakfast", is_healthy=True),
    FoodItemCreate(name="Trứng bác", serving_size="2 quả trứng", calories=155, protein=13, carbs=1, fat=11, fiber=0, category="breakfast", is_healthy=True),
    FoodItemCreate(name="Sữa chua Hy Lạp với mật ong", serving_size="1 cốc", calories=220, protein=20, carbs=30, fat=2, fiber=0, category="breakfast", is_healthy=True),
    FoodItemCreate(name="Bánh mì nguyên cám với bơ đậu phộng", serving_size="2 lát", calories=280, protein=10, carbs=28, fat=14, fiber=4, category="breakfast", is_healthy=True),
    FoodItemCreate(name="Chuối với hạnh nhân", serving_size="1 quả chuối + 28g hạnh nhân", calories=250, protein=9, carbs=27, fat=14, fiber=4, category="breakfast", is_healthy=True),

    # Bữa trưa
    FoodItemCreate(name="Ức gà nướng với bông cải xanh", serving_size="150g + 1 cốc", calories=280, protein=35, carbs=15, fat=5, fiber=3, category="lunch", is_healthy=True),
    FoodItemCreate(name="Cá hồi với khoai lang", serving_size="150g + 1 củ vừa", calories=320, protein=28, carbs=25, fat=14, fiber=3, category="lunch", is_healthy=True),
    FoodItemCreate(name="Bánh wrap gà tây và rau", serving_size="1 cuốn", calories=350, protein=25, carbs=38, fat=12, fiber=5, category="lunch", is_healthy=True),
    FoodItemCreate(name="Bát quinoa với rau", serving_size="1 cốc", calories=400, protein=15, carbs=52, fat=8, fiber=6, category="lunch", is_healthy=True),
    FoodItemCreate(name="Salad cá ngừ với dầu ô liu", serving_size="150g + 2 muỗng canh dầu", calories=350, protein=32, carbs=8, fat=20, fiber=3, category="lunch", is_healthy=True),

    # Bữa tối
    FoodItemCreate(name="Thịt bò nạc với cơm gạo lứt", serving_size="150g + 1 cốc", calories=380, protein=32, carbs=42, fat=9, fiber=2, category="dinner", is_healthy=True),
    FoodItemCreate(name="Cá rô phi với măng tây", serving_size="150g + 1 cốc", calories=220, protein=28, carbs=8, fat=9, fiber=2, category="dinner", is_healthy=True),
    FoodItemCreate(name="Gà xào với cơm gạo lứt", serving_size="150g gà + 1 cốc", calories=420, protein=30, carbs=48, fat=12, fiber=4, category="dinner", is_healthy=True),
    FoodItemCreate(name="Mì pasta với thịt gà tây xay", serving_size="1 cốc mì + 150g thịt", calories=450, protein=32, carbs=52, fat=11, fiber=3, category="dinner", is_healthy=True),
    FoodItemCreate(name="Thịt heo thăn nướng với rau", serving_size="150g + 2 cốc", calories=300, protein=32, carbs=18, fat=10, fiber=4, category="dinner", is_healthy=True),

    # Ăn vặt
    FoodItemCreate(name="Thanh protein", serving_size="1 thanh", calories=200, protein=20, carbs=18, fat=6, fiber=2, category="snacks", is_healthy=True),
    FoodItemCreate(name="Táo với bơ hạnh nhân", serving_size="1 quả táo + 1 muỗng canh", calories=190, protein=4, carbs=25, fat=8, fiber=4, category="snacks", is_healthy=True),
    FoodItemCreate(name="Hỗn hợp hạt", serving_size="28g", calories=160, protein=6, carbs=6, fat=14, fiber=3, category="snacks", is_healthy=True),
    FoodItemCreate(name="Sinh tố protein", serving_size="1 ly (250ml)", calories=180, protein=25, carbs=15, fat=2, fiber=0, category="snacks", is_healthy=True),
    FoodItemCreate(name="Bánh gạo với mật ong", serving_size="2 bánh + 1 muỗng canh", calories=150, protein=2, carbs=32, fat=1, fiber=1, category="snacks", is_healthy=True),
    FoodItemCreate(name="Sữa chua Hy Lạp", serving_size="1 cốc (170g)", calories=100, protein=17, carbs=7, fat=0, fiber=0, category="snacks", is_healthy=True),

    # Rau
    FoodItemCreate(name="Salad rau bina", serving_size="2 cốc", calories=14, protein=2, carbs=2, fat=0, fiber=1, category="vegetables", is_healthy=True),
    FoodItemCreate(name="Bông cải xanh", serving_size="1 cốc sống", calories=31, protein=3, carbs=6, fat=0, fiber=2, category="vegetables", is_healthy=True),
    FoodItemCreate(name="Cà rốt", serving_size="1 củ vừa", calories=25, protein=1, carbs=6, fat=0, fiber=1, category="vegetables", is_healthy=True),
    FoodItemCreate(name="Ớt chuông", serving_size="1 quả vừa", calories=37, protein=1, carbs=9, fat=0, fiber=2, category="vegetables", is_healthy=True),
    FoodItemCreate(name="Dưa leo", serving_size="1 quả vừa", calories=45, protein=2, carbs=11, fat=0, fiber=2, category="vegetables", is_healthy=True),

    # Trái cây
    FoodItemCreate(name="Chuối", serving_size="1 quả vừa", calories=105, protein=1, carbs=27, fat=0, fiber=3, category="fruits", is_healthy=True),
    FoodItemCreate(name="Táo", serving_size="1 quả vừa", calories=95, protein=0, carbs=25, fat=0, fiber=4, category="fruits", is_healthy=True),
    FoodItemCreate(name="Việt quất", serving_size="1 cốc", calories=85, protein=1, carbs=21, fat=0, fiber=3, category="fruits", is_healthy=True),
    FoodItemCreate(name="Cam", serving_size="1 quả vừa", calories=62, protein=1, carbs=15, fat=0, fiber=3, category="fruits", is_healthy=True),
    FoodItemCreate(name="Dâu tây", serving_size="1 cốc", calories=49, protein=1, carbs=12, fat=0, fiber=3, category="fruits", is_healthy=True),

    # Protein nạc
    FoodItemCreate(name="Ức gà (đã nấu)", serving_size="100g", calories=165, protein=31, carbs=0, fat=3, fiber=0, category="lean_protein", is_healthy=True),
    FoodItemCreate(name="Ức gà tây (đã nấu)", serving_size="100g", calories=135, protein=30, carbs=0, fat=1, fiber=0, category="lean_protein", is_healthy=True),
    FoodItemCreate(name="Cá rô phi (đã nấu)", serving_size="100g", calories=96, protein=20, carbs=0, fat=1, fiber=0, category="lean_protein", is_healthy=True),
    FoodItemCreate(name="Cá hồi (đã nấu)", serving_size="100g", calories=208, protein=22, carbs=0, fat=13, fiber=0, category="lean_protein", is_healthy=True),
    FoodItemCreate(name="Cá ngừ (đóng hộp, ngâm nước)", serving_size="100g", calories=99, protein=23, carbs=0, fat=0, fiber=0, category="lean_protein", is_healthy=True),

    # Ngũ cốc nguyên hạt
    FoodItemCreate(name="Gạo lứt (đã nấu)", serving_size="1 cốc", calories=216, protein=5, carbs=45, fat=2, fiber=3, category="whole_grains", is_healthy=True),
    FoodItemCreate(name="Yến mạch (đã nấu)", serving_size="1 cốc", calories=150, protein=5, carbs=27, fat=3, fiber=4, category="whole_grains", is_healthy=True),
    FoodItemCreate(name="Bánh mì nguyên cám", serving_size="1 lát", calories=80, protein=4, carbs=14, fat=1, fiber=2, category="whole_grains", is_healthy=True),
    FoodItemCreate(name="Quinoa (đã nấu)", serving_size="1 cốc", calories=222, protein=8, carbs=39, fat=4, fiber=5, category="whole_grains", is_healthy=True),
    FoodItemCreate(name="Mì nguyên cám (đã nấu)", serving_size="1 cốc", calories=174, protein=7, carbs=37, fat=1, fiber=6, category="whole_grains", is_healthy=True),

    # Sữa
    FoodItemCreate(name="Sữa ít béo", serving_size="1 cốc", calories=102, protein=8, carbs=12, fat=2, fiber=0, category="dairy", is_healthy=True),
    FoodItemCreate(name="Phô mai ít béo", serving_size="28g", calories=49, protein=7, carbs=0, fat=2, fiber=0, category="dairy", is_healthy=True),
    FoodItemCreate(name="Phô mai tươi (cottage) ít béo", serving_size="1 cốc", calories=163, protein=28, carbs=6, fat=2, fiber=0, category="dairy", is_healthy=True),

    # Các loại hạt
    FoodItemCreate(name="Hạnh nhân", serving_size="28g", calories=164, protein=6, carbs=6, fat=14, fiber=3, category="nuts", is_healthy=True),
    FoodItemCreate(name="Hạt điều", serving_size="28g", calories=155, protein=5, carbs=9, fat=12, fiber=1, category="nuts", is_healthy=True),
]
    
    try:
        for food_data in foods_data:
            existing_food = db.query(FoodItem).filter(FoodItem.name == food_data.name).first()
            if not existing_food:
                CRUDNutrition.add_food_item(db, food_data)
        
        print(f"✅ Successfully seeded {len(foods_data)} food items!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("📊 Database tables created")
    
    # Seed data
    seed_food_database()
