from sqlalchemy.orm import Session
from datetime import date
from model.nutrition_model import FoodItem, NutritionDay
from crud.crud_nutrition import CRUDNutrition, CRUDSleep
from model.user_model import user
import random


class AINutritionService:
    """AI-powered nutrition recommendation system"""
    
    # Macro ratios for different fitness goals
    MACRO_RATIOS = {
        "weight_loss": {"protein": 0.33, "carbs": 0.42, "fat": 0.25},
        "muscle_gain": {"protein": 0.35, "carbs": 0.45, "fat": 0.20},
        "maintenance": {"protein": 0.30, "carbs": 0.50, "fat": 0.20},
        "endurance": {"protein": 0.25, "carbs": 0.60, "fat": 0.15},
    }
    
    # Calorie multipliers based on activity level
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    # tinh toán nhu cầu calo hàng ngày dựa trên hồ sơ người dùng (cân nặng, chiều cao, tuổi, giới tính) và mức độ hoạt động thể chất của họ
    @staticmethod
    def calculate_bmr(weight: float, height: int, age: int, gender: str = "M") -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor formula"""
        if gender.upper() == "M":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr
    
    # tính target calo hàng ngày dựa trên mục tiêu thể dục của người dùng (giảm cân, tăng cơ, duy trì, hoặc cải thiện sức bền) và mức độ hoạt động của họ
    @staticmethod
    def calculate_daily_calories(user_obj: user) -> float:
        """Calculate daily calorie needs based on user profile"""  
        bmr = AINutritionService.calculate_bmr(
            user_obj.weight, 
            user_obj.height, 
            user_obj.age,
            user_obj.sex
        )
        multiplier = AINutritionService.ACTIVITY_MULTIPLIERS.get(user_obj.activity_level, 1.55)
        print(f"Calculated BMR: {bmr}, Activity Multiplier: {multiplier} for user_id={user_obj.id}")
        return bmr * multiplier
    
    @staticmethod
    def get_fitness_goal(db: Session, user_id: int) -> str:
        """Determine fitness goal based on user activity"""
        nutrition_day = CRUDNutrition.get_daily_nutrition(db, user_id, date.today())
        
        if not nutrition_day:
            return "maintenance"
        
        calorie_deficit = nutrition_day.calories_burned - nutrition_day.calories_consumed
        
        if calorie_deficit > 300:
            return "weight_loss"
        elif calorie_deficit < -300:
            return "muscle_gain"
        elif nutrition_day.calories_burned > 500:
            return "endurance"
        else:
            return "maintenance"
    
    @staticmethod
    def get_nutrition_recommendation(
        db: Session,
        user_obj: user,
        user_id: int,
        activity_level: str = "moderate"
    ):
        """Generate personalized nutrition recommendations"""
        
        # Calculate daily calorie goal
        daily_calories = AINutritionService.calculate_daily_calories(user_obj)
        
        # Get fitness goal
        fitness_goal = AINutritionService.get_fitness_goal(db, user_id)
        
        # Get macro ratios
        macros = AINutritionService.MACRO_RATIOS.get(fitness_goal, AINutritionService.MACRO_RATIOS["maintenance"])
        
        # Calculate macro grams (1g protein/carbs = 4 cal, 1g fat = 9 cal)
        protein_grams = (daily_calories * macros["protein"]) / 4
        carbs_grams = (daily_calories * macros["carbs"]) / 4
        fat_grams = (daily_calories * macros["fat"]) / 9
        water_liters = max(2.0, user_obj.weight / 30)  # 1L per 30kg
        
        # Get recommended foods
        recommended_foods = AINutritionService._get_recommended_foods(
            db, fitness_goal, daily_calories
        )
        
        return {
            "daily_calorie_goal": round(daily_calories, 0),
            "protein_grams": round(protein_grams, 1),
            "carbs_grams": round(carbs_grams, 1),
            "fat_grams": round(fat_grams, 1),
            "water_liters": round(water_liters, 1),
            "recommended_meals": recommended_foods,
            "fitness_goal": fitness_goal,
            "activity_level": activity_level,
            "explanation": AINutritionService._get_explanation(fitness_goal, daily_calories, water_liters)
        }
    
    @staticmethod
    def _get_recommended_foods(db: Session, goal: str, daily_calories: float, top_n: int = 8):
        """Get recommended foods based on fitness goal"""
        
        # Define category priorities based on goal
        category_priority = {
            "weight_loss": ["lean_protein", "vegetables", "fruits", "whole_grains"],
            "muscle_gain": ["lean_protein", "whole_grains", "dairy", "nuts"],
            "endurance": ["whole_grains", "fruits", "lean_protein", "vegetables"],
            "maintenance": ["lean_protein", "whole_grains", "vegetables", "fruits"]
        }
        
        priority = category_priority.get(goal, category_priority["maintenance"])
        foods = []
        
        for category in priority:
            category_foods = CRUDNutrition.get_foods_by_category(db, category)
            foods.extend(category_foods[:3])
        
        return foods[:top_n] if foods else CRUDNutrition.get_healthy_foods(db, top_n)
    
    @staticmethod
    def _get_explanation(goal: str, calories: float, water: float) -> str:
        """Generate explanation for recommendations"""
        explanations = {
            "giảm cân": f"Based on your activity, aim for {calories:.0f} calories daily with higher protein to preserve muscle. Drink {water:.1f}L water.",
            "tăng cân": f"For endurance training, {calories:.0f} calories with carbs focus for energy. Stay hydrated with {water:.1f}L water.",
            "duy trì cân nặng": f"For balanced health, aim for {calories:.0f} calories daily. Maintain hydration with {water:.1f}L water."
        }
        return explanations.get(goal, explanations["maintenance"])
    
    # hàm tạo một menu hàng ngày hoàn chỉnh với các món ăn được chọn dựa trên nhu cầu calo hàng ngày và mục tiêu thể dục của người dùng, đảm bảo cân bằng dinh dưỡng và đa dạng thực phẩm
    @staticmethod
    def generate_daily_menu(db: Session, daily_calories: float, goal: str = "maintenance"):
        """Generate a complete day's menu"""
        
        # Calorie distribution: breakfast 25%, lunch 35%, dinner 30%, snacks 10%
        calories_distribution = {
            "breakfast": daily_calories * 0.25,
            "lunch": daily_calories * 0.35,
            "dinner": daily_calories * 0.30,
            "snacks": daily_calories * 0.10
        }
        
        menu = {}
        for meal_type, target_calories in calories_distribution.items():
            menu[meal_type] = AINutritionService._select_foods_for_meal(
                db, meal_type, target_calories
            )
        
        # Calculate totals
        total_nutrition = AINutritionService._calculate_menu_totals(menu)
        
        return {
            "breakfast": menu.get("breakfast", []),
            "lunch": menu.get("lunch", []),
            "dinner": menu.get("dinner", []),
            "snacks": menu.get("snacks", []),
            **total_nutrition
        }
    # hàm tạo bửa ăn cho một bữa cụ thể (ví dụ: bữa sáng, bữa trưa, bữa tối) dựa trên nhu cầu calo mục tiêu cho bữa đó và mục tiêu thể dục của người dùng, đảm bảo lựa chọn thực phẩm phù hợp với mục tiêu và sở thích của người dùng
    @staticmethod
    def _select_foods_for_meal(db: Session, meal_type: str, target_calories: float):
        """Select foods for a specific meal"""
        foods = CRUDNutrition.get_foods_by_category(db, meal_type)
        random.shuffle(foods)  # Shuffle to add variety
        selected = []
        current_calories = 0
        
        for food in foods:
            if current_calories + food.calories <= target_calories+50:
                selected.append(food)
                current_calories += food.calories
        
        return selected if selected else CRUDNutrition.get_foods_by_category(db, meal_type)[:2]
    
    @staticmethod
    def _calculate_menu_totals(menu: dict):
        """Calculate total nutrition for menu"""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for meal_foods in menu.values():
            if isinstance(meal_foods, list):
                for food in meal_foods:
                    total_calories += food.calories
                    total_protein += food.protein
                    total_carbs += food.carbs
                    total_fat += food.fat
        
        return {
            "total_calories": round(total_calories, 0),
            "total_protein": round(total_protein, 1),
            "total_carbs": round(total_carbs, 1),
            "total_fat": round(total_fat, 1)
        }
    
    @staticmethod
    def get_sleep_recommendation(db: Session, user_id: int) -> dict:
        """Get sleep recommendations based on activity"""
        sleep_stats = CRUDSleep.get_sleep_statistics(db, user_id, 30)
        
        if not sleep_stats:
            return {
                "recommended_hours": 8,
                "current_average": 0,
                "recommendation": "Start tracking sleep to get personalized insights"
            }
        
        current_avg = sleep_stats.get("average_sleep", 0)
        recommended = 8  # Standard recommendation
        
        if current_avg < 6:
            recommendation = "You're getting insufficient sleep. Try to aim for 7-9 hours."
        elif current_avg < 7:
            recommendation = "Increase sleep to 7-8 hours for optimal recovery."
        elif current_avg > 9:
            recommendation = "You might be oversleeping. Aim for 7-9 hours for best results."
        else:
            recommendation = "Great! Your sleep duration is optimal."
        
        return {
            "recommended_hours": recommended,
            "current_average": round(current_avg, 1),
            "recommendation": recommendation,
            "consistency": sleep_stats.get("consistency", 0)
        }
