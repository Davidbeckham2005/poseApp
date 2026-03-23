# 🎯 Quick Start Guide - AI Nutrition System

## ⚡ 5-Minute Setup

### Step 1: Seed Database
```bash
cd python
python seed_nutrition.py
```
Output: "✅ Successfully seeded 50+ food items!"

### Step 2: Verify Backend is Running
```bash
uvicorn main:app --reload
```

### Step 3: Access Wellness Page
Navigate to: `http://localhost:5173/#/wellness`

## 📱 User Interface

### Main Features

#### 🍎 Nutrition Tab
- **AI Recommendation Card**: Shows personalized daily targets
  - Daily Calorie Goal
  - Protein, Carbs, Fat grams
  - Water intake
  
- **Daily Menu Suggestion**: Complete meal plan
  - 🌅 Breakfast
  - 🥗 Lunch  
  - 🍖 Dinner
  - 🍌 Snacks
  - Total nutrition totals

#### 😴 Sleep Tab
- **Sleep Recommendations**: Based on your activity
  - Recommended hours
  - Current average
  - Consistency score
  
- **Sleep Tips**: Optimization strategies
  - Schedule consistency
  - Environment optimization
  - Screen time management
  - Exercise timing

#### 📅 Schedule Tab
- **Weekly View**: 7-day calendar
- **Today's Activities**: Chronological listing
  - Time & duration
  - Activity type with emoji
  - Status (pending/completed)

## 🔧 Common Tasks

### Log a Meal
1. Navigate to Daily Menu
2. Click on meal section
3. Select food items from database
4. System auto-calculates nutrition

### Track Sleep
1. Go to Sleep tab
2. Enter bedtime & wake time
3. Rate sleep quality
4. Add optional notes
5. View sleep history

### Schedule a Workout
1. Go to Schedule tab
2. Click "Add Activity"
3. Fill: Date, Time, Duration
4. Select activity type
5. Set reminder if needed
6. Mark as completed when done

### Get Menu Suggestions
- System auto-generates based on:
  - Your calorie target
  - Fitness goal (detected from activity)
  - Available foods in database
  - Meal time distribution

## 📊 Key Metrics

### Daily Dashboard Shows
- **Calories**: Consumed vs. Target vs. Burned
- **Macros**: Protein, Carbs, Fat (grams)
- **Water**: Daily intake tracking (liters)
- **Sleep**: Hours, quality, consistency

### Fitness Goals Auto-Detected
- **Weight Loss**: -300 cal deficit
- **Muscle Gain**: +300 cal surplus
- **Endurance**: 500+ cal burned
- **Maintenance**: Balanced

## 💡 AI Features

### Smart Macro Adjustment
System automatically adjusts based on:
- Exercise type & intensity
- Time since last workout
- Sleep quality
- Current fitness level

### Personalized Recommendations
- Considers user BMI & BMR
- Adapts to activity level
- Suggests optimal protein/carbs/fat
- Recommends hydration levels

### Meal Planning
- Distributes calories:
  - Breakfast: 25%
  - Lunch: 35%
  - Dinner: 30%
  - Snacks: 10%
- Selects healthy options
- Prevents repetition

## 🔌 API Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| Get Recommendation | `/api/nutrition/recommend/{user_id}` | GET |
| Get Menu | `/api/nutrition/menu/{user_id}` | GET |
| Log Meal | `/api/nutrition/user/{user_id}/meals` | POST |
| Get Sleep Stats | `/api/nutrition/sleep/stats/{user_id}` | GET |
| Log Sleep | `/api/nutrition/sleep/{user_id}` | POST |
| Get Schedule | `/api/nutrition/schedule/{user_id}/today` | GET |
| Create Schedule | `/api/nutrition/schedule/{user_id}` | POST |

## 🎨 Customization Tips

### Change Daily Calorie Target
Edit `crud_nutrition.py` line ~28:
```python
nutrition_day.calories_target = 2200  # Set your default
```

### Add New Food Category
1. Add entry to seed_nutrition.py
2. Create FoodItemCreate() with category
3. Re-run: `python seed_nutrition.py`

### Modify Activity Multiplier
Edit `nutrition_service.py` ACTIVITY_MULTIPLIERS:
```python
"my_level": 1.65  # Custom activity multiplier
```

### Adjust Macro Ratios
Edit `nutrition_service.py` MACRO_RATIOS:
```python
"my_goal": {"protein": 0.40, "carbs": 0.40, "fat": 0.20}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No foods showing | Run `python seed_nutrition.py` |
| "User not found" | Ensure you're logged in |
| Menu not generating | Check user has complete profile |
| API 404 errors | Verify user_id in URL |
| Recommendations same daily | Try changing activity_level param |

## 📈 Measuring Progress

### Track Over Time
- Sleep consistency %
- Average daily calories
- Macro distribution adherence
- Schedule completion rate

### Best Practices
- Log meals immediately after eating
- Record sleep same time daily
- Check schedule weekly
- Review recommendations monthly

## 🚀 Advanced Features

### Activity Level Options
```
?activity_level=sedentary     # 1.2x multiplier
?activity_level=light          # 1.375x multiplier
?activity_level=moderate       # 1.55x multiplier (default)
?activity_level=active         # 1.725x multiplier
?activity_level=very_active    # 1.9x multiplier
```

### Sleep Statistics
```
GET /api/nutrition/sleep/stats/1?days=30
Returns: avg_sleep, consistency%, last_7_days_avg
```

### Weekly Schedule
```
GET /api/nutrition/schedule/week/1/2024-03-18
Returns: All activities for week starting March 18
```

## 📝 Database Schema Quick View

```
FoodItem (50+ items)
  ├─ name, serving_size
  ├─ calories, protein, carbs, fat, fiber
  └─ category, is_healthy

NutritionDay (per date)
  ├─ calories_consumed, calories_burned
  ├─ protein_grams, carbs_grams, fat_grams
  └─ water_liters, updated_at

SleepRecord (per night)
  ├─ bedtime, wake_time, sleep_hours
  ├─ sleep_quality (poor/fair/good/excellent)
  └─ notes, date

ScheduleEntry (activities)
  ├─ date, time, duration
  ├─ activity, activity_type
  ├─ status (pending/completed/skipped)
  └─ reminder_enabled
```

## 🎓 Understanding the AI

### Algorithm Flow
1. **Collect User Data**: Weight, height, age, DOB
2. **Calculate BMR**: Using Mifflin-St Jeor formula
3. **Apply Activity Multiplier**: Based on exercise intensity
4. **Detect Goal**: By analyzing calorie deficit/surplus
5. **Assign Macros**: From goal-specific ratios
6. **Generate Menu**: Distribute calories across meals
7. **Provide Recommendations**: With personalized tips

### Example Calculation
```
User: 70kg, 175cm, 25yr, active
BMR = 10(70) + 6.25(175) - 5(25) + 5 = 1755 kcal
Daily = 1755 × 1.725 = 3027 kcal
Goal Detection: Calories burned > 500 → Endurance
Macros: 25% protein, 60% carbs, 15% fat
```

## ✅ Success Checklist

- [ ] Backend running with uvicorn
- [ ] Database seeded with foods
- [ ] Frontend can access /wellness page
- [ ] User profile complete (weight, height, DOB)
- [ ] Can view nutrition recommendations
- [ ] Can see daily menu suggestion
- [ ] Can log meals
- [ ] Can track sleep
- [ ] Can create schedule entries

---

**🎉 You're now ready to use the AI Nutrition System!**
