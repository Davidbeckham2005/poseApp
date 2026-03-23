<template>
    <div class="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white p-6">
        <!-- Header with Welcome -->
        <div class="mb-8">
            <h1 class="text-4xl font-bold mb-2">Welcome, {{ userName }}! 👋</h1>
            <p class="text-gray-400">{{ getGreeting() }}</p>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-gradient-to-br from-blue-600/20 to-blue-900/20 rounded-lg p-6 border border-blue-500/30">
                <p class="text-gray-400 text-sm mb-2">Total Workouts</p>
                <p class="text-3xl font-bold text-blue-400">{{ stats.totalWorkouts }}</p>
                <p class="text-gray-500 text-xs mt-2">This month</p>
            </div>
            
            <div class="bg-gradient-to-br from-green-600/20 to-green-900/20 rounded-lg p-6 border border-green-500/30">
                <p class="text-gray-400 text-sm mb-2">Avg Accuracy</p>
                <p class="text-3xl font-bold text-green-400">{{ stats.avgAccuracy }}%</p>
                <p class="text-gray-500 text-xs mt-2">Form quality</p>
            </div>
            
            <div class="bg-gradient-to-br from-orange-600/20 to-orange-900/20 rounded-lg p-6 border border-orange-500/30">
                <p class="text-gray-400 text-sm mb-2">Calories Burned</p>
                <p class="text-3xl font-bold text-orange-400">{{ stats.caloriesBurned }}</p>
                <p class="text-gray-500 text-xs mt-2">This week</p>
            </div>
            
            <div class="bg-gradient-to-br from-purple-600/20 to-purple-900/20 rounded-lg p-6 border border-purple-500/30">
                <p class="text-gray-400 text-sm mb-2">Streak</p>
                <p class="text-3xl font-bold text-purple-400">{{ stats.dayStreak }}</p>
                <p class="text-gray-500 text-xs mt-2">Days active</p>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold mb-4">Quick Actions</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button @click="navigateTo('game')" class="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 rounded-lg p-6 font-semibold transition-all flex items-center gap-3">
                    <span class="text-2xl">🏋️</span>
                    <div class="text-left">
                        <div>Start Workout</div>
                        <div class="text-sm text-red-200">Fitness Adventure</div>
                    </div>
                </button>
                
                <button @click="navigateTo('wellness')" class="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 rounded-lg p-6 font-semibold transition-all flex items-center gap-3">
                    <span class="text-2xl">🍎</span>
                    <div class="text-left">
                        <div>Nutrition</div>
                        <div class="text-sm text-green-200">View recommendations</div>
                    </div>
                </button>
                
                <button @click="navigateTo('upload')" class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 rounded-lg p-6 font-semibold transition-all flex items-center gap-3">
                    <span class="text-2xl">📹</span>
                    <div class="text-left">
                        <div>Check Form</div>
                        <div class="text-sm text-blue-200">Upload workout video</div>
                    </div>
                </button>
            </div>
        </div>

        <!-- Recent Activity -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold mb-4">Recent Activity</h2>
            <div class="bg-gray-800/50 rounded-lg border border-gray-700">
                <div v-if="recentActivities.length === 0" class="p-8 text-center text-gray-400">
                    <p>No recent activities. Start your first workout! 🚀</p>
                </div>
                <div v-else>
                    <div v-for="(activity, idx) in recentActivities" :key="idx" :class="[
                        'p-4 border-b border-gray-700 last:border-b-0 flex justify-between items-center',
                        idx % 2 === 0 ? 'bg-gray-800/30' : ''
                    ]">
                        <div>
                            <p class="font-semibold">{{ activity.name }}</p>
                            <p class="text-sm text-gray-400">{{ activity.date }}</p>
                        </div>
                        <div class="text-right">
                            <p class="text-blue-400 font-bold">{{ activity.reps }}</p>
                            <p class="text-sm text-gray-400">{{ activity.accuracy }}% accuracy</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Goal Section -->
        <div class="bg-gradient-to-r from-indigo-600/20 to-purple-600/20 rounded-lg border border-indigo-500/30 p-6">
            <h2 class="text-2xl font-bold mb-4">Today's Goal</h2>
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-300 mb-2">Complete 3 workout sessions</p>
                    <div class="w-48 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" :style="{ width: goalProgress + '%' }"></div>
                    </div>
                    <p class="text-sm text-gray-400 mt-2">{{ goalProgress }}% complete</p>
                </div>
                <button class="bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-lg font-semibold transition-all">
                    View Goals →
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useNavigation } from '../../composable/helpers';

const { switch_on_sidebar } = useNavigation();

// Sample data
const userName = ref('User');

// Statistics
const stats = ref({
    totalWorkouts: 24,
    avgAccuracy: 85,
    caloriesBurned: 1250,
    dayStreak: 7
});

// Recent activities
const recentActivities = ref([
    { name: 'Push-ups', date: 'Today, 10:30 AM', reps: '20 reps', accuracy: '88%' },
    { name: 'Squats', date: 'Today, 9:00 AM', reps: '15 reps', accuracy: '92%' },
    { name: 'Plank', date: 'Yesterday, 5:00 PM', reps: '45 sec', accuracy: '78%' },
    { name: 'Lunges', date: 'Yesterday, 4:00 PM', reps: '12 reps', accuracy: '84%' },
]);

const goalProgress = ref(67);

// Methods
const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning! Ready to workout? 💪';
    if (hour < 18) return 'Afternoon check-in! Keep up the momentum! 🔥';
    return 'Evening workout session? Let\'s finish strong! 🌙';
};

const navigateTo = (tab) => {
    switch_on_sidebar(tab);
};
</script>

<style scoped>
/* Custom animations */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

div {
    animation: slideInUp 0.5s ease-out;
}
</style>
