import { api } from "../api";
export const nutritionApi = {
    getRecommendation: async (userId) =>
        (await api.get(`api/nutrition/recommend/${userId}`)).data,

    getMenu: async (userId) =>
        (await api.get(`api/nutrition/menu/${userId}`)).data,

    getSleepRecommendation: async (userId) =>
        (await api.get(`api/nutrition/sleep/recommendation/${userId}`)).data,

    getTodaySchedule: async (userId) =>
        (await api.get(`api/nutrition/schedule/${userId}/today`)).data,

    getDailyNutrition: async (userId, date) =>
        (await api.get(`api/nutrition/user/${userId}/nutrition/${date}`)).data,

    getRecentSleep: async (userId, days) =>
        (await api.get(`api/nutrition/sleep/recent/${userId}?days=${days}`)).data,

    logMeal: async (userId, data) =>
        (await api.post(`api/nutrition/user/${userId}/meals`, data)).data,

    logSleep: async (userId, data) =>
        (await api.post(`api/nutrition/sleep/${userId}`, data)).data,

    createSchedule: async (userId, data) =>
        (await api.post(`api/nutrition/schedule/${userId}`, data)).data,

    markScheduleComplete: async (entryId) =>
        (await api.patch(`api/nutrition/schedule/${entryId}/complete`)).data,
    get_all_food_items: async () =>
        (await api.get(`api/nutrition/foods/get_all`)).data,
    update_calories_burned: async (userId, caloriesBurnData) =>
        (await api.post(`api/nutrition/user/${userId}/nutrition/calories_burned`, caloriesBurnData)).data,
    get_nutrition_all: async (userId, startDate, endDate) =>
        (await api.get(`api/nutrition/user/${userId}/nutrition/all`, {
            params: {
                start_date: startDate,
                end_date: endDate
            }
        })).data,
}