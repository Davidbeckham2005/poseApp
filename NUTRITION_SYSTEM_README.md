# AI Nutrition, Sleep & Wellness System

## 📋 Overview

This comprehensive wellness system integrates AI-powered nutrition recommendations, sleep tracking, and activity scheduling into your PoseApp.

## ✨ Features

### 🍎 AI Nutrition System
- **Personalized Calorie Calculation**: Based on BMR, weight, height, and activity level
- **Smart Macro Distribution**: Automatic protein/carbs/fat ratios based on fitness goals
  - Weight Loss: High protein (33%), moderate carbs (42%), low fat (25%)
  - Muscle Gain: High protein (35%), balanced carbs (45%), low fat (20%)
  - Endurance: Low protein (25%), high carbs (60%), low fat (15%)
  - Maintenance: Balanced macros (30/50/20)

- **Daily Menu Generation**: AI suggests complete daily menus:
  - Breakfast (25% daily calories)
  - Lunch (35% daily calories)
  - Dinner (30% daily calories)
  - Snacks (10% daily calories)

- **Food Tracking**: Log meals and track nutrition intake
- **50+ Pre-loaded Foods**: Database includes common healthy foods across categories
- **Calorie/Macro Database**: Each food item includes detailed nutrition info

### 😴 Sleep Tracking & Analysis
- **Sleep Record Logging**: Track bedtime, wake time, and sleep quality
- **Sleep Duration Calculation**: Automatic hourly calculation
- **Sleep Statistics**: 
  - Average sleep duration
  - Sleep consistency percentage
  - Weekly trends
- **AI Sleep Recommendations**: Based on exercise intensity and recovery needs
- **Sleep Optimization Tips**: Personalized guidance for better sleep

### 📅 Activity Scheduling
- **Daily/Weekly Scheduling**: Plan workouts, meals, rest days
- **Activity Types**: Workout, meal time, rest, walks, yoga, strength training
- **Status Tracking**: Mark activities as pending, completed, or skipped
- **Reminder System**: Enable/disable reminders for scheduled activities
- **Calendar View**: Visual weekly schedule

## 🚀 Getting Started

### 1. Initialize Database

Run the seed script to populate food database:

```bash
cd PoseApp/python
python seed_nutrition.py
```

### 2. Backend Setup

The nutrition router is automatically included. Just ensure your main.py is updated:

```python
from routers import nutrition_router
app.include_router(nutrition_router.router)
```

### 3. Frontend Integration

Add the Wellness component to your router:

```javascript
{
    path: '/wellness',
    name: 'wellness',
    component: () => import('@/component/layout/Wellness.vue')
}
```

## 📡 API Endpoints

### Nutrition Endpoints
- `POST /api/nutrition/foods` - Add new food item
- `GET /api/nutrition/foods/category/{category}` - Get foods by category
- `GET /api/nutrition/foods/healthy` - Get healthy foods
- `POST /api/nutrition/user/{user_id}/meals` - Log a meal
- `GET /api/nutrition/user/{user_id}/nutrition/{date}` - Get daily nutrition
- `GET /api/nutrition/recommend/{user_id}` - Get AI recommendations
- `GET /api/nutrition/menu/{user_id}` - Get daily menu suggestion

### Sleep Endpoints
- `POST /api/nutrition/sleep/{user_id}` - Log sleep
- `GET /api/nutrition/sleep/{user_id}/{date}` - Get sleep record
- `GET /api/nutrition/sleep/stats/{user_id}` - Get sleep statistics
- `GET /api/nutrition/sleep/recommendation/{user_id}` - Get sleep recommendations
- `GET /api/nutrition/sleep/recent/{user_id}` - Get recent sleep records (7-30 days)

### Schedule Endpoints
- `POST /api/nutrition/schedule/{user_id}` - Create schedule entry
- `PUT /api/nutrition/schedule/{entry_id}` - Update schedule entry
- `GET /api/nutrition/schedule/{user_id}/{date}` - Get daily schedule
- `GET /api/nutrition/schedule/week/{user_id}/{start_date}` - Get weekly schedule
- `PATCH /api/nutrition/schedule/{entry_id}/complete` - Mark as completed
- `DELETE /api/nutrition/schedule/{entry_id}` - Delete schedule entry
- `GET /api/nutrition/schedule/{user_id}/today` - Get today's schedule

## 💾 Database Models

### NutritionDay
Tracks daily nutrition intake and targets

### FoodItem
Pre-loaded food database with 50+ items across categories

### MealLog
User's meal entries with timestamps

### SleepRecord
Sleep tracking records with quality metrics

### ScheduleEntry
Scheduled activities and workouts

## 🎯 AI Algorithm Details

### Calorie Calculation (Mifflin-St Jeor Formula)
```
BMR = 10×weight(kg) + 6.25×height(cm) - 5×age(years) + 5
Daily Calories = BMR × Activity Multiplier
```

**Activity Multipliers:**
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Active: 1.725
- Very Active: 1.9

### Goal Detection
- **Weight Loss**: Calorie deficit > 300
- **Muscle Gain**: Calorie deficit < -300
- **Endurance**: Calories burned > 500
- **Maintenance**: Default

### Sleep Consistency Score
Calculated based on sleep duration variance across 30 days (0-100%)

## 📝 Usage Examples

### Get Nutrition Recommendation
```javascript
GET /api/nutrition/recommend/1?activity_level=active
```

Response:
```json
{
  "daily_calorie_goal": 2500,
  "protein_grams": 200,
  "carbs_grams": 275,
  "fat_grams": 83,
  "water_liters": 3.2,
  "fitness_goal": "muscle_gain",
  "recommendation": "To build muscle, consume..."
}
```

### Log a Meal
```javascript
POST /api/nutrition/user/1/meals
{
  "food_id": 5,
  "servings": 1,
  "meal_time": "2024-03-19T12:30:00",
  "notes": "Lunch at office"
}
```

### Log Sleep
```javascript
POST /api/nutrition/sleep/1
{
  "date": "2024-03-19",
  "bedtime": "23:00",
  "wake_time": "07:00",
  "sleep_quality": "good",
  "notes": "Slept well"
}
```

### Create Schedule Entry
```javascript
POST /api/nutrition/schedule/1
{
  "date": "2024-03-19",
  "time": "08:00",
  "activity": "Morning Run",
  "duration": 30,
  "activity_type": "workout",
  "description": "5k run in park"
}
```

## 🔄 Integration with PoseApp

The system automatically integrates with your existing exercise tracking:

1. **Calories Burned**: Automatically calculated from exercise sessions
2. **Goal Detection**: System adapts recommendations based on your workouts
3. **Time Integration**: Schedule system syncs with your exercise routine
4. **Recovery Tracking**: Sleep data used to optimize exercise suggestions

## 🛠️ Customization

### Add Custom Foods
```bash
POST /api/nutrition/foods
{
  "name": "Your Food",
  "serving_size": "100g",
  "calories": 200,
  "protein": 10,
  "carbs": 20,
  "fat": 8,
  "category": "lunch",
  "is_healthy": true
}
```

### Modify Macro Ratios
Edit `services/nutrition_service.py`:
```python
MACRO_RATIOS = {
    "your_goal": {"protein": 0.35, "carbs": 0.45, "fat": 0.20}
}
```

### Change Default Calorie Target
Edit the nutrition day creation in `crud/crud_nutrition.py`:
```python
nutrition_day.calories_target = 2500  # Your target
```

## 📊 Frontend Components

### Wellness.vue
Main dashboard component with three tabs:
- **Nutrition**: AI recommendations + daily menu
- **Sleep**: Sleep analysis + optimization tips
- **Schedule**: Weekly calendar + today's activities

### Pinia Store (wellness.store.js)
- Centralized state management
- API integration helpers
- Loading/error handling

## 🔐 Data Security

- User data is isolated by user_id
- No sensitive health data in URLs (except IDs)
- Database uses SQLite with secure connections

## 📈 Future Enhancements

- [ ] Social features (meal sharing, challenges)
- [ ] Advanced analytics dashboard
- [ ] Integration with popular fitness trackers
- [ ] Photo-based food recognition
- [ ] Meal prep suggestions
- [ ] Recipe database
- [ ] Macro tracking charts
- [ ] Export health reports
- [ ] Mobile app version
- [ ] Cloud backup

## 🐛 Troubleshooting

### Foods Not Showing Up
```bash
python seed_nutrition.py
```

### Schedule Not Loading
Check if user_id is correct and accessible

### Recommendations Not Personalizing
Ensure user profile has complete data:
- Weight (kg)
- Height (cm)
- Date of birth

### API Errors
Check CORS settings in main.py includes your frontend origin

## 📞 Support

For issues or feature requests, update the system components as needed.
