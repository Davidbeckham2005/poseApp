import { defineStore } from "pinia";
import { ref } from "vue";
import { nutritionApi } from "../services/nutrition_api.services";

export const useWellness = defineStore('wellness', () => {
    const nutritionRecommendation = ref(null)
    const dailyMenu = ref(null)
    const sleepRecommendation = ref(null)
    const todaySchedule = ref([])
    const dailyNutrition = ref(null)
    const recentSleepRecords = ref([])
    const listFoodItems = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchNutritionRecommendation = async (userId, activityLevel = 'moderate') => {
        loading.value = true
        try {
            // const response = await api.get(`/nutrition/recommend/${userId}?activity_level=${activityLevel}`)
            const response = await nutritionApi.getRecommendation(userId, activityLevel)
            nutritionRecommendation.value = response.data
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching nutrition recommendation:', err)
        } finally {
            loading.value = false
        }
    }
    const get_all_food_items = async () => {
        loading.value = true
        try {
            const response = await nutritionApi.get_all_food_items()
            console.log('All Food Items:', response)
            listFoodItems.value = response
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching all food items:', err)
        } finally {
            loading.value = false
        }
    }
    const fetchDailyMenu = async (userId, activityLevel = 'moderate') => {
        loading.value = true
        try {
            const response = await nutritionApi.getMenu(userId, activityLevel)
            dailyMenu.value = response
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching daily menu:', err)
        } finally {
            loading.value = false
        }
    }

    const fetchSleepRecommendation = async (userId) => {
        loading.value = true
        try {
            const response = await nutritionApi.getSleepRecommendation(userId)
            sleepRecommendation.value = response.data
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching sleep recommendation:', err)
        } finally {
            loading.value = false
        }
    }

    const fetchTodaySchedule = async (userId) => {
        loading.value = true
        try {
            const response = await nutritionApi.getTodaySchedule(userId)
            todaySchedule.value = response.data.entries || []
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching today schedule:', err)
        } finally {
            loading.value = false
        }
    }
    // lấy thông tin dinh dưỡng tổng quan của một ngày cụ thể, bao gồm tổng calo, protein, carbs, fat đã tiêu thụ và các bữa ăn đã log trong ngày đó
    const fetchDailyNutrition = async (userId, date) => {
        loading.value = true
        console.log(`Fetching daily nutrition for userId=${userId} on date=${date}`)
        try {
            const response = await nutritionApi.getDailyNutrition(userId, date)
            console.log('Daily Nutrition Data:', response)
            dailyNutrition.value = response
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching daily nutrition:', err)
        } finally {
            loading.value = false
        }
    }

    const fetchRecentSleep = async (userId, days = 7) => {
        loading.value = true
        try {
            const response = await nutritionApi.getRecentSleep(userId, days)
            recentSleepRecords.value = response.data
            error.value = null
        } catch (err) {
            error.value = err.message
            console.error('Error fetching recent sleep:', err)
        } finally {
            loading.value = false
        }
    }

    const logMeal = async (userId, mealData) => {
        try {
            const response = await nutritionApi.logMeal(userId, mealData)
            return response
        } catch (err) {
            error.value = err.message
            console.error('Error logging meal:', err)
            return null
        }
    }

    const logSleep = async (userId, sleepData) => {
        try {
            const response = await nutritionApi.logSleep(userId, sleepData)
            return response
        } catch (err) {
            error.value = err.message
            console.error('Error logging sleep:', err)
            return null
        }
    }

    const createScheduleEntry = async (userId, entryData) => {
        try {
            const response = await api.post(`/nutrition/schedule/${userId}`, entryData)
            return response.data
        } catch (err) {
            error.value = err.message
            console.error('Error creating schedule entry:', err)
            return null
        }
    }

    const markScheduleComplete = async (entryId) => {
        try {
            const response = await nutritionApi.markScheduleComplete(entryId)
            return response
        } catch (err) {
            error.value = err.message
            console.error('Error marking schedule complete:', err)
            return null
        }
    }

    return {
        nutritionRecommendation,
        dailyMenu,
        sleepRecommendation,
        todaySchedule,
        dailyNutrition,
        recentSleepRecords,
        loading,
        error,
        fetchNutritionRecommendation,
        fetchDailyMenu,
        fetchSleepRecommendation,
        fetchTodaySchedule,
        fetchDailyNutrition,
        fetchRecentSleep,
        logMeal,
        logSleep,
        createScheduleEntry,
        markScheduleComplete,
        get_all_food_items,
        listFoodItems
    }
})
