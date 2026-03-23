import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '../api/index';

export const useFitness = defineStore('fitness', () => {
    const workouts = ref([]);
    const goals = ref([]);
    const exercises = ref([]);
    const progressStats = ref(null);
    const loading = ref(false);
    const error = ref(null);

    // ========== Workout Management ==========
    const fetchWorkouts = async (userId, limit = 50) => {
        loading.value = true;
        try {
            // This will call the schedule endpoint to get workout entries
            const response = await api.get(`/nutrition/schedule/${userId}`);
            workouts.value = response.data.entries || [];
            error.value = null;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching workouts:', err);
        } finally {
            loading.value = false;
        }
    };

    const logWorkout = async (userId, workoutData) => {
        try {
            const scheduleData = {
                activity_type: workoutData.exerciseName,
                date: new Date(workoutData.date).toISOString().split('T')[0],
                time: new Date(workoutData.date).toTimeString().split(' ')[0],
                duration: workoutData.duration,
                notes: `${workoutData.intensity} intensity | ${workoutData.notes || ''}`
            };

            const response = await api.post(`/nutrition/schedule/${userId}`, scheduleData);
            if (response.data) {
                workouts.value.unshift(response.data);
            }
            error.value = null;
            return response.data;
        } catch (err) {
            error.value = err.message;
            console.error('Error logging workout:', err);
            return null;
        }
    };

    const updateWorkout = async (workoutId, updateData) => {
        try {
            const response = await api.patch(`/nutrition/schedule/${workoutId}`, updateData);
            const index = workouts.value.findIndex(w => w.id === workoutId);
            if (index !== -1) {
                workouts.value[index] = response.data;
            }
            error.value = null;
            return response.data;
        } catch (err) {
            error.value = err.message;
            console.error('Error updating workout:', err);
            return null;
        }
    };

    const deleteWorkout = async (workoutId) => {
        try {
            await api.delete(`/nutrition/schedule/${workoutId}`);
            workouts.value = workouts.value.filter(w => w.id !== workoutId);
            error.value = null;
            return true;
        } catch (err) {
            error.value = err.message;
            console.error('Error deleting workout:', err);
            return false;
        }
    };

    const completeWorkout = async (workoutId) => {
        try {
            const response = await api.patch(`/nutrition/schedule/${workoutId}/complete`);
            const index = workouts.value.findIndex(w => w.id === workoutId);
            if (index !== -1) {
                workouts.value[index] = response.data;
            }
            error.value = null;
            return response.data;
        } catch (err) {
            error.value = err.message;
            console.error('Error completing workout:', err);
            return null;
        }
    };

    // ========== Fitness Goals Management ==========
    const fetchGoals = async (userId) => {
        loading.value = true;
        try {
            // Goals could be stored as schedule entries with type 'goal'
            // Or we could extend the backend to have a dedicated goals endpoint
            // For now, we'll use local storage or a fictional endpoint
            const storedGoals = localStorage.getItem(`fitness_goals_${userId}`);
            if (storedGoals) {
                goals.value = JSON.parse(storedGoals);
            }
            error.value = null;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching goals:', err);
        } finally {
            loading.value = false;
        }
    };

    const createGoal = async (userId, goalData) => {
        try {
            // Save goal to local storage (extend backend later if needed)
            const newGoal = {
                id: Date.now(),
                ...goalData,
                createdAt: new Date().toISOString()
            };
            goals.value.push(newGoal);

            // Persist to local storage
            localStorage.setItem(`fitness_goals_${userId}`, JSON.stringify(goals.value));
            error.value = null;
            return newGoal;
        } catch (err) {
            error.value = err.message;
            console.error('Error creating goal:', err);
            return null;
        }
    };

    const updateGoal = async (userId, goalId, updateData) => {
        try {
            const index = goals.value.findIndex(g => g.id === goalId);
            if (index !== -1) {
                goals.value[index] = { ...goals.value[index], ...updateData };
                localStorage.setItem(`fitness_goals_${userId}`, JSON.stringify(goals.value));
            }
            error.value = null;
            return goals.value[index];
        } catch (err) {
            error.value = err.message;
            console.error('Error updating goal:', err);
            return null;
        }
    };

    const deleteGoal = async (userId, goalId) => {
        try {
            goals.value = goals.value.filter(g => g.id !== goalId);
            localStorage.setItem(`fitness_goals_${userId}`, JSON.stringify(goals.value));
            error.value = null;
            return true;
        } catch (err) {
            error.value = err.message;
            console.error('Error deleting goal:', err);
            return false;
        }
    };

    // ========== Exercises Database ==========
    const fetchExercises = async (category = null) => {
        loading.value = true;
        try {
            // Could fetch from a backend endpoint in the future
            // For now, using predefined exercises
            exercises.value = getDefaultExercises();
            if (category) {
                exercises.value = exercises.value.filter(e => e.category === category);
            }
            error.value = null;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching exercises:', err);
        } finally {
            loading.value = false;
        }
    };

    const getDefaultExercises = () => {
        return [
            {
                id: 1,
                name: 'Push-ups',
                description: 'Classic upper body exercise targeting chest, shoulders, and triceps',
                difficulty: 'Beginner',
                category: 'Strength',
                muscleGroup: 'Chest, Shoulders, Triceps',
                caloriesPerRep: 0.32,
                recommended: '3x10',
                duration: 30,
                equipment: 'Bodyweight'
            },
            {
                id: 2,
                name: 'Squats',
                description: 'Lower body strength exercise for legs and glutes',
                difficulty: 'Intermediate',
                category: 'Strength',
                muscleGroup: 'Legs, Glutes',
                caloriesPerRep: 0.5,
                recommended: '3x15',
                duration: 45,
                equipment: 'Bodyweight'
            },
            {
                id: 3,
                name: 'Plank',
                description: 'Core stability and endurance exercise',
                difficulty: 'Beginner',
                category: 'Core',
                muscleGroup: 'Core',
                caloriesPerRep: 0.2,
                recommended: '3x30-60s',
                duration: 60,
                equipment: 'Bodyweight'
            },
            {
                id: 4,
                name: 'Lunges',
                description: 'Single leg strength and balance exercise',
                difficulty: 'Intermediate',
                category: 'Strength',
                muscleGroup: 'Legs, Glutes',
                caloriesPerRep: 0.4,
                recommended: '3x12',
                duration: 40,
                equipment: 'Bodyweight'
            },
            {
                id: 5,
                name: 'Running',
                description: 'Cardio and endurance training',
                difficulty: 'Intermediate',
                category: 'Cardio',
                muscleGroup: 'Full Body',
                caloriesPerRep: 10,
                recommended: '30-45 mins',
                duration: 45,
                equipment: 'None'
            },
            {
                id: 6,
                name: 'Jumping Jacks',
                description: 'Full body cardio exercise for warm-ups and endurance',
                difficulty: 'Beginner',
                category: 'Cardio',
                muscleGroup: 'Full Body',
                caloriesPerRep: 0.17,
                recommended: '3x20',
                duration: 30,
                equipment: 'Bodyweight'
            },
            {
                id: 7,
                name: 'Shoulder Stretch',
                description: 'Flexibility and mobility exercise',
                difficulty: 'Beginner',
                category: 'Stretching',
                muscleGroup: 'Shoulders',
                caloriesPerRep: 0.1,
                recommended: '3x30s',
                duration: 20,
                equipment: 'Bodyweight'
            },
            {
                id: 8,
                name: 'Burpees',
                description: 'Full body high-intensity exercise combining strength and cardio',
                difficulty: 'Advanced',
                category: 'Strength + Cardio',
                muscleGroup: 'Full Body',
                caloriesPerRep: 0.75,
                recommended: '3x10',
                duration: 25,
                equipment: 'Bodyweight'
            },
            {
                id: 9,
                name: 'Mountain Climbers',
                description: 'Core and cardio exercise',
                difficulty: 'Intermediate',
                category: 'Core + Cardio',
                muscleGroup: 'Core, Cardio',
                caloriesPerRep: 0.3,
                recommended: '3x20',
                duration: 35,
                equipment: 'Bodyweight'
            },
            {
                id: 10,
                name: 'Cycling',
                description: 'Low-impact cardio exercise',
                difficulty: 'Beginner',
                category: 'Cardio',
                muscleGroup: 'Legs, Full Body',
                caloriesPerRep: 8,
                recommended: '30-60 mins',
                duration: 45,
                equipment: 'Bicycle'
            }
        ];
    };

    // ========== Progress & Statistics ==========
    const fetchProgressStats = async (userId, timeRange = 'week') => {
        loading.value = true;
        try {
            const stats = calculateProgressStats(userId, timeRange);
            progressStats.value = stats;
            error.value = null;
            return stats;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching progress stats:', err);
        } finally {
            loading.value = false;
        }
    };

    const calculateProgressStats = (userId, timeRange) => {
        const rangeInDays = {
            'week': 7,
            'month': 30,
            '3months': 90
        };

        const days = rangeInDays[timeRange] || 7;
        const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);

        const filteredWorkouts = workouts.value.filter(w => {
            const workoutDate = new Date(w.date || w.createdAt);
            return workoutDate >= cutoffDate;
        });

        const totalCalories = filteredWorkouts.reduce((sum, w) => sum + (w.calories || 0), 0);
        const totalDuration = filteredWorkouts.reduce((sum, w) => sum + (w.duration || 0), 0);
        const avgDuration = filteredWorkouts.length > 0 ? Math.round(totalDuration / filteredWorkouts.length) : 0;

        // Get favorite exercise
        const exerciseCount = {};
        filteredWorkouts.forEach(w => {
            const exerciseType = w.activity_type || w.exerciseName || 'Unknown';
            exerciseCount[exerciseType] = (exerciseCount[exerciseType] || 0) + 1;
        });

        let favoriteExercise = null;
        let maxCount = 0;
        for (const [exercise, count] of Object.entries(exerciseCount)) {
            if (count > maxCount) {
                maxCount = count;
                favoriteExercise = { name: exercise, count };
            }
        }

        return {
            totalWorkouts: filteredWorkouts.length,
            totalCalories: Math.round(totalCalories),
            totalDuration,
            avgDuration,
            avgIntensity: 'Moderate',
            favoriteExercise,
            timeRange
        };
    };

    // ========== Get Recommendations ==========
    const getExerciseRecommendations = async (userId, fitnessLevel = 'beginner') => {
        try {
            // Could call an AI backend endpoint for personalized recommendations
            const allExercises = getDefaultExercises();
            const levelMap = {
                'beginner': ['Beginner'],
                'intermediate': ['Beginner', 'Intermediate'],
                'advanced': ['Beginner', 'Intermediate', 'Advanced']
            };

            const recommendations = allExercises
                .filter(e => levelMap[fitnessLevel].includes(e.difficulty))
                .sort(() => Math.random() - 0.5)
                .slice(0, 5);

            return recommendations;
        } catch (err) {
            error.value = err.message;
            console.error('Error getting recommendations:', err);
            return [];
        }
    };

    // Reset all data
    const reset = () => {
        workouts.value = [];
        goals.value = [];
        exercises.value = [];
        progressStats.value = null;
        loading.value = false;
        error.value = null;
    };

    return {
        // State
        workouts,
        goals,
        exercises,
        progressStats,
        loading,
        error,

        // Workout methods
        fetchWorkouts,
        logWorkout,
        updateWorkout,
        deleteWorkout,
        completeWorkout,

        // Goal methods
        fetchGoals,
        createGoal,
        updateGoal,
        deleteGoal,

        // Exercise methods
        fetchExercises,
        getDefaultExercises,

        // Stats methods
        fetchProgressStats,
        getExerciseRecommendations,

        // Utility
        reset
    };
});
