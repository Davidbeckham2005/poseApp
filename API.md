# food method
## get category by category type
- method: get
- eg http://127.0.0.1:8000/api/nutrition/foods/category/lunch
- return data, array
[
  {
    "name": "Grilled chicken breast with broccoli",
    "serving_size": "150g + 1 cup",
    "calories": 280.0,
    "protein": 35.0,
    "carbs": 15.0,
    "fat": 5.0,
    "fiber": 3.0,
    "category": "lunch",
    "is_healthy": true,
    "id": 6,
    "created_at": "2026-03-19T16:53:12.556327"
  },
]
## get healthy food
- method: get
- eg: http://127.0.0.1:8000/api/nutrition/foods/healthy
- return: [
  {
    "name": "Oatmeal with berries",
    "serving_size": "1 cup",
    "calories": 200.0,
    "protein": 6.0,
    "carbs": 35.0,
    "fat": 4.0,
    "fiber": 5.0,
    "category": "breakfast",
    "is_healthy": true,
    "id": 1,
    "created_at": "2026-03-19T16:53:12.529328"
  },
]
## about nutrion
### get daily nutrion on day
- method: get
- path: http://127.0.0.1:8000/api/nutrition/user/1/nutrition/2026-3-20
- return data: {
  "id": 1,
  "date": "2026-03-20",
  "calories_consumed": 400.0,
  "calories_burned": 0.0,
  "calories_target": 2000.0,
  "protein_grams": 12.0,
  "carbs_grams": 70.0,
  "fat_grams": 8.0,
  "water_liters": 0.0
}
## about meal
### create a daily meal
- method: post
- body: {
  "food_id": 1,
  "notes" :"I'am so hurry"
}
- return: {
  "id": 3,
  "user_id": 1,
  "food_id": 1,
  "servings": 1.0,
  "meal_time": "2026-03-20T12:57:33.492983",
  "notes": "I'am so hurry"
}
- path: http://127.0.0.1:8000/api/nutrition/user/1/meals
### get a daily meal on day
- method: get
- path: http://127.0.0.1:8000/api/nutrition/user/1/meals/2026-3-20
- return: {
  [
  {
    "id": 1,
    "user_id": 1,
    "food_id": 1,
    "servings": 1.0,
    "meal_time": "2026-03-20T11:19:01.944407",
    "notes": null
  },
  {
    "id": 2,
    "user_id": 1,
    "food_id": 1,
    "servings": 1.0,
    "meal_time": "2026-03-20T11:19:11.896237",
    "notes": "I'am so hurry"
  },
  {
    "id": 3,
    "user_id": 1,
    "food_id": 1,
    "servings": 1.0,
    "meal_time": "2026-03-20T12:57:33.492983",
    "notes": "I'am so hurry"
  }
]
}
# recommend method
## get menu for a day 
method: get
path: http://127.0.0.1:8000/api/nutrition/menu/1
return: {
  "breakfast": [
    {
      "name": "Oatmeal with berries",
      "serving_size": "1 cup",
      "calories": 200.0,
      "protein": 6.0,
      "carbs": 35.0,
      "fat": 4.0,
      "fiber": 5.0,
      "category": "breakfast",
      "is_healthy": true,
      "id": 1,
      "created_at": "2026-03-19T16:53:12.529328"
    },
    {
      "name": "Scrambled eggs",
      "serving_size": "2 eggs",
      "calories": 155.0,
      "protein": 13.0,
      "carbs": 1.0,
      "fat": 11.0,
      "fiber": 0.0,
      "category": "breakfast",
      "is_healthy": true,
      "id": 2,
      "created_at": "2026-03-19T16:53:12.537328"
    },
    {
      "name": "Greek yogurt with honey",
      "serving_size": "1 cup",
      "calories": 220.0,
      "protein": 20.0,
      "carbs": 30.0,
      "fat": 2.0,
      "fiber": 0.0,
      "category": "breakfast",
      "is_healthy": true,
      "id": 3,
      "created_at": "2026-03-19T16:53:12.543337"
    }
  ],
  "lunch": [
    {
      "name": "Grilled chicken breast with broccoli",
      "serving_size": "150g + 1 cup",
      "calories": 280.0,
      "protein": 35.0,
      "carbs": 15.0,
      "fat": 5.0,
      "fiber": 3.0,
      "category": "lunch",
      "is_healthy": true,
      "id": 6,
      "created_at": "2026-03-19T16:53:12.556327"
    },
    {
      "name": "Salmon with sweet potato",
      "serving_size": "150g + 1 medium",
      "calories": 320.0,
      "protein": 28.0,
      "carbs": 25.0,
      "fat": 14.0,
      "fiber": 3.0,
      "category": "lunch",
      "is_healthy": true,
      "id": 7,
      "created_at": "2026-03-19T16:53:12.559328"
    },
    {
      "name": "Turkey and vegetable wrap",
      "serving_size": "1 wrap",
      "calories": 350.0,
      "protein": 25.0,
      "carbs": 38.0,
      "fat": 12.0,
      "fiber": 5.0,
      "category": "lunch",
      "is_healthy": true,
      "id": 8,
      "created_at": "2026-03-19T16:53:12.562327"
    }
  ],
  "dinner": [
    {
      "name": "Lean beef with brown rice",
      "serving_size": "150g + 1 cup",
      "calories": 380.0,
      "protein": 32.0,
      "carbs": 42.0,
      "fat": 9.0,
      "fiber": 2.0,
      "category": "dinner",
      "is_healthy": true,
      "id": 11,
      "created_at": "2026-03-19T16:53:12.572325"
    },
    {
      "name": "Tilapia with asparagus",
      "serving_size": "150g + 1 cup",
      "calories": 220.0,
      "protein": 28.0,
      "carbs": 8.0,
      "fat": 9.0,
      "fiber": 2.0,
      "category": "dinner",
      "is_healthy": true,
      "id": 12,
      "created_at": "2026-03-19T16:53:12.576330"
    }
  ],
  "snacks": [
    {
      "name": "Protein bar",
      "serving_size": "1 bar",
      "calories": 200.0,
      "protein": 20.0,
      "carbs": 18.0,
      "fat": 6.0,
      "fiber": 2.0,
      "category": "snacks",
      "is_healthy": true,
      "id": 16,
      "created_at": "2026-03-19T16:53:12.589840"
    },
    {
      "name": "Mixed nuts",
      "serving_size": "1 oz (23g)",
      "calories": 160.0,
      "protein": 6.0,
      "carbs": 6.0,
      "fat": 14.0,
      "fiber": 3.0,
      "category": "snacks",
      "is_healthy": true,
      "id": 18,
      "created_at": "2026-03-19T16:53:12.598141"
    }
  ],
  "total_calories": 2485.0,
  "total_protein": 213.0,
  "total_carbs": 218.0,
  "total_fat": 86.0
}
- process
1. get user_id
2. calculating daily_caloris, fitness goals depend on user and activity_level