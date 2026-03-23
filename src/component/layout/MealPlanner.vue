<template>
    <div class="min-h-screen dark:g-gradient-to-b from-gray-900 dark:to-black text-white p-6">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8 text-black dark:text-white">
            <h1 class="text-4xl font-bold">Bửa ăn & Dinh dưỡng</h1>
            <button @click="showProfileModal = true"
                class="bg-blue-600 hover:bg-blue-500     px-6 py-2 rounded-lg font-semibold transition-all flex items-center gap-2">
                Chỉnh Sửa Hồ Sơ
            </button>
        </div>

        <!-- User Profile Card -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 text-black dark:text-white">
            <div class="dark:bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <p class="text-gray-400 text-sm">Trọng lượng</p>
                <p class="text-2xl font-bold dark:text-blue-400">{{ userProfile.weight }} kg</p>
                <p class="text-gray-400 text-sm">Chiều cao</p>
                <p class="text-2xl font-bold dark:text-green-400">{{ userProfile.height }} cm</p>
            </div>

            <div class="dark:bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <p class="text-gray-400 text-sm">Mục tiêu cân nặng</p>
                <p class="text-2xl font-bold dark:text-orange-400">{{ userProfile.target_weight }} kg</p>
                <span class="text-gray-400 text-sm">{{ userProfile.goal }}</span>
            </div>
            <div class="dark:bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <p class="text-gray-400 text-sm">Chỉ số BMI</p>
                <p class="text-2xl font-bold dark:text-purple-400">{{ userProfile.BMI }}</p>
                <p class="text-gray-400 text-sm">Tình trạng</p>
                <p class="text-2xl font-bold dark:text-red-400">{{ userProfile.typeBMI }}</p>
            </div>

        </div>
        <!-- Daily Nutrition Summary -->
        <div class="dark:bg-gray-800/50 rounded-xl border border-indigo-500/30 p-8">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold">Tóm tắt Dinh dưỡng Ngày</h2>
                <span>{{ userProfile.date }}</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div class="bg-black/40 rounded-lg p-4">
                    <p class="text-sm text-gray-400 mb-2">Total Calories</p>
                    <p class="text-3xl font-bold text-yellow-400">{{ calculateTotalNutrition().calories }}</p>
                </div>
                <div class="bg-black/40 rounded-lg p-4">
                    <p class="text-sm text-gray-400 mb-2">Protein</p>
                    <p class="text-3xl font-bold text-red-400">{{ calculateTotalNutrition().protein }}g</p>
                </div>
                <div class="bg-black/40 rounded-lg p-4">
                    <p class="text-sm text-gray-400 mb-2">Carbs</p>
                    <p class="text-3xl font-bold text-blue-400">{{ calculateTotalNutrition().carbs }}g</p>
                </div>
                <div class="bg-black/40 rounded-lg p-4">
                    <p class="text-sm text-gray-400 mb-2">Fat</p>
                    <p class="text-3xl font-bold text-orange-400">{{ calculateTotalNutrition().fat }}g</p>
                </div>
                <div class="bg-black/40 rounded-lg p-4">
                    <p class="text-sm text-gray-400 mb-2">Goal</p>
                    <p class="text-3xl font-bold text-purple-400">{{ userProfile.dailyCalorieGoal }}</p>
                </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-6">
                <div class="flex justify-between mb-2">
                    <span>Dinh dưỡng hôm nay</span>
                    <span class="font-bold">{{ calculateTotalNutrition().calories }} / {{ userProfile.dailyCalorieGoal
                    }} cal</span>
                </div>
                <div class="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-green-500 to-blue-500 rounded-full transition-all"
                        :style="{ width: Math.min((calculateTotalNutrition().calories / userProfile.dailyCalorieGoal) * 100, 100) + '%' }">
                    </div>
                </div>
            </div>
            <!-- <div class="mt-6">
                <div class="flex justify-between mb-2">
                    <span>Caloris tiêu thụ</span>
                    <span class="font-bold">{{ calculateTotalNutrition().calories }} / {{ userProfile.dailyCalorieGoal
                        }} cal</span>
                </div>
                <div class="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-green-500 to-blue-500 rounded-full transition-all"
                        :style="{ width: Math.min((calculateTotalNutrition().calories / userProfile.dailyCalorieGoal) * 100, 100) + '%' }">
                    </div>
                </div>
            </div> -->
        </div>
        <div class="mb-8">
            <h2 class="text-2xl font-bold mb-4 mt-4">Bửa ăn khuyến nghị</h2>
            <span @click="get_menu_handle"
                class="px-4 py-3 rounded-lg font-semibold transition-all cursor-pointer hover:scale-105"
                :class="selectedBuoi ? 'bg-gradient-to-r from-blue-600 to-cyan-500 shadow-lg' : 'bg-gray-800 hover:bg-gray-700'">Nhận
                menu </span>
            <div class="space-y-6 mt-5 bg-gray-900 p-4 rounded-xl">
                <div class="grid grid-cols-4 gap-2 mb-6 bg-gray-900/50 p-3 rounded-xl border border-gray-700">
                    <div class="text-center">
                        <p class="text-[10px] text-gray-400 uppercase">Calories</p>
                        <p class="text-lg font-bold text-yellow-500">{{ recommend_menu.total_calories }}</p>
                    </div>
                    <div class="text-center border-l border-gray-700">
                        <p class="text-[10px] text-gray-400 uppercase">Protein</p>
                        <p class="text-lg font-bold text-red-500">{{ recommend_menu.total_protein }}g</p>
                    </div>
                    <div class="text-center border-l border-gray-700">
                        <p class="text-[10px] text-gray-400 uppercase">Carbs</p>
                        <p class="text-lg font-bold text-blue-500">{{ recommend_menu.total_carbs }}g</p>
                    </div>
                    <div class="text-center border-l border-gray-700">
                        <p class="text-[10px] text-gray-400 uppercase">Fat</p>
                        <p class="text-lg font-bold text-orange-500">{{ recommend_menu.total_fat }}g</p>
                    </div>
                </div>
                <div v-for="mealType in ['breakfast', 'lunch', 'dinner', 'snacks']" :key="mealType">

                    <div v-if="recommend_menu[mealType].length != 0"
                        class="flex justify-between items-center mb-2 px-1 border-b border-gray-800 pb-1">
                        <h3 class="text-xs font-black uppercase text-gray-500 tracking-widest">{{ mealType }}</h3>
                        <button @click="addNewFoodHandle(mealType)"
                            class="text-[10px] font-bold text-blue-500 hover:text-blue-400">
                            + THÊM MÓN
                        </button>
                    </div>

                    <div class="space-y-2">
                        <div v-for="(meal, idx) in recommend_menu[mealType]" :key="idx"
                            class="flex justify-between items-center bg-black/40 p-3 rounded-lg hover:bg-black/60 transition-all border border-transparent hover:border-gray-800 group">

                            <div class="flex-1 min-w-0">
                                <p class="font-semibold text-xl flex items-center gap-2"> {{ meal.name }} - {{
                                    meal.serving_size }}
                                </p>
                            </div>

                            <div class="text-right mr-4 shrink-0">
                                <p class="font-bold text-yellow-400 text-sm">{{ meal.calories }} cal</p>
                                <p class="text-[9px] text-gray-600">P: {{ meal.protein }}g | C: {{ meal.carbs }}g</p>
                            </div>

                            <div class="flex gap-1 shrink-0">
                                <button @click="remakeSingleFood(mealType, idx)"
                                    class="bg-gray-800 hover:bg-gray-700 p-2 rounded-lg transition-all" title="Đổi món">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-400" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4 4v5h5m11 11v-5h-5m1.1-12.4a9 9 0 11-15.5 2L4 9" />
                                    </svg>
                                </button>

                                <button @click="removeFood(mealType, idx)"
                                    class="bg-red-900/40 hover:bg-red-600 p-2 rounded-lg transition-all group/btn"
                                    title="Xóa">
                                    <svg xmlns="http://www.w3.org/2000/svg"
                                        class="h-4 w-4 text-red-500 group-hover/btn:text-white" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Choose Meals Section -->


    <!-- All Meals Selected Today -->
    <!-- <div class="mb-8">
        <h2 class="text-2xl font-bold mb-4">📅 Today's Meals</h2>
        <div class="bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-xl border border-purple-500/30 p-6">
            <div v-if="selectedBuoi.length === 0" class="text-center text-gray-400 py-8">
                <p>No meals selected yet. Add meals to see them here! 👇</p>
            </div>
            <div v-else>
                <div class="space-y-3">
                    <div v-for="(meal, idx) in selectedMeals" :key="idx"
                        class="flex justify-between items-center bg-black/40 p-4 rounded-lg">
                        <div class="flex-1">
                            <p class="font-semibold">{{ meal.emoji }} {{ meal.name }}</p>
                            <p class="text-sm text-gray-400">{{ meal.description }}</p>
                        </div>
                        <div class="text-right mr-4">
                            <p class="font-semibold text-yellow-400">{{ meal.calories }} cal</p>
                        </div>
                        <button @click="removeMealFromDay(idx)"
                            class="bg-red-600 hover:bg-red-500 px-3 py-2 rounded-lg transition-all">
                            Remove
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div> -->
    <!-- Edit Profile Modal -->
    <!-- thêm món ăn vào menu -->
    <div v-if="showAddFoodModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 min-h-screen">
        <div
            class="w-full max-w-5xl h-[85vh] bg-gray-900 rounded-xl shadow-xl flex flex-col p-4 overflow-scroll bar-thin border border-gray-700">
            <div class="flex justify-between mb-4">
                <h2 class="text-2xl font-bold ">Chọn bửa ăn của bạn</h2>
                <span>
                    <x @click="showAddFoodModal = false"
                        class="text-red-400 cursor-pointer hover:scale-105 transition-all"></x>
                </span>
            </div>
            <!-- Meal Category Tabs -->
            <div :class="!ShowFilterModal ? '' : 'bg-gray-800/70 border border-gray-700 rounded-lg p-4 mb-6 min-w-4xl'">
                <div>
                    <span @click="ShowFilterModal = !ShowFilterModal"
                        class="px-4 py-2 rounded-lg font-semibold transition-all"
                        :class="!ShowFilterModal ? 'bg-gradient-to-r from-blue-600 to-cyan-500 shadow-lg' : 'bg-gray-800 hover:bg-gray-700'">Bộ
                        lọc </span>
                </div>
                <div v-if="ShowFilterModal"
                    class="flex-wrap items-center justify-center z-50 transition-all mt-4 mb-6 space-x-0.5">
                    <button v-for="category in mealCategories" :key="category" @click="selectedCategory = category"
                        :class="[
                            'px-4 py-2 rounded-lg font-semibold transition-all',
                            selectedCategory === category
                                ? 'bg-gradient-to-r from-blue-600 to-cyan-500 shadow-lg'
                                : 'bg-gray-800 hover:bg-gray-700'
                        ]">
                        {{ category }}
                    </button>
                </div>
            </div>

            <!-- Meals Grid -->
            <div class="flex justify-center items-center space-x-2 mb-6 min-w-4xl">
                <button @click="currentPage--" :disabled="currentPage === 1"
                    class="px-3 py-1 bg-gray-700 rounded disabled:opacity-50"> Trước </button>

                <span class="text-sm">Trang {{ currentPage }} / {{ page }}</span>

                <button @click="currentPage++" :disabled="currentPage === page"
                    class="px-3 py-1 bg-gray-700 rounded disabled:opacity-50"> Sau </button>
            </div>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 min-w-4xl">
                <div v-for="food in paginatedItems" :key="food.id">
                    <div
                        class="p-2 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-blue-500 transition-all overflow-hidden">
                        <div class="relative h-24 w-full bg-gray-700">
                            <img :src="`https://picsum.photos/seed/${food.id}/200/200`"
                                class="w-full h-full object-cover" alt="food image" loading="lazy" />
                        </div>
                        <p class="text-sm font-bold truncate mb-1" :title="food.name">{{ food.name }}</p>

                        <p class="text-xs text-yellow-400 font-bold mb-2">{{ food.calories }} kcal/{{ food.serving_size
                        }}

                        </p>

                        <div class="grid grid-cols-2 gap-x-1 gap-y-1 text-[10px] mb-3">
                            <div class="flex flex-col">
                                <span class="text-gray-500 uppercase">Protein</span>
                                <span class="text-red-400 font-medium">{{ food.protein }}g</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="text-gray-500 uppercase">Carbs</span>
                                <span class="text-blue-400 font-medium">{{ food.carbs }}g</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="text-gray-500 uppercase">Fat</span>
                                <span class="text-orange-400 font-medium">{{ food.fat }}g</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="text-gray-500 uppercase">Fiber</span>
                                <span class="text-emerald-400 font-medium">{{ food.fiber }}g</span>
                            </div>
                        </div>

                        <button @click="addMealToDay(food); addNewFood(food)" :class="[
                            'w-full py-1.5 rounded text-xs font-bold transition-all',
                            selectedMeals.some(m => m.id === food.id)
                                ? 'bg-green-600 text-white'
                                : 'bg-blue-600/80 hover:bg-blue-500 text-white'
                        ]">
                            {{selectedMeals.some(m => m.id === food.id) ? '✓' : '+ Add'}}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- chỉnh sửa hồ sơ -->
    <div v-if="showProfileModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
        <div class="bg-gray-800 rounded-xl p-8 max-w-md w-full border border-gray-700">
            <h2 class="text-2xl font-bold mb-6">Chỉnh Sửa Hồ Sơ</h2>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Giới tính</label>
                    <select v-model="editProfileData.sex" type="text"
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500 appearance-none">
                        <option value="" disabled selected>Chọn giới tính</option>
                        <option value="M">Nam</option>
                        <option value="F">Nữ</option>
                        <option value="other">Khác</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Tuổi</label>
                    <input v-model="editProfileData.day_of_birth" type="date"
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Trọng Lượng (kg)</label>
                    <input v-model.number="editProfileData.weight" type="number"
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Chiều Cao (cm)</label>
                    <input v-model.number="editProfileData.height" type="number"
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Trọng Lượng Mục Tiêu (kg)</label>
                    <input v-model.number="editProfileData.target_weight" type="number"
                        class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm text-gray-400 mb-2">Mức độ hoạt động</label>
                    <div class="relative">
                        <select v-model="editProfileData.activity_level"
                            class="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500 appearance-none cursor-pointer">
                            <option value="sedentary">Ít vận động (Văn phòng, ít tập thể dục)</option>
                            <option value="light">Vận động nhẹ (Tập 1-3 ngày/tuần)</option>
                            <option value="moderate">Vận động vừa (Tập 3-5 ngày/tuần)</option>
                            <option value="active">Vận động mạnh (Tập 6-7 ngày/tuần)</option>
                            <option value="very_active">Vận động rất mạnh (Tập nặng, vận động viên)</option>
                        </select>
                        <div
                            class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-400">
                            <svg class="fill-current h-4 w-4" viewBox="0 0 20 20">
                                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-3 mt-8">
                <button @click="saveProfile"
                    class="flex-1 bg-blue-600 hover:bg-blue-500 py-2 rounded-lg font-semibold transition-all">
                    Luu Thay Đổi
                </button>
                <button @click="showProfileModal = false"
                    class="flex-1 bg-gray-700 hover:bg-gray-600 py-2 rounded-lg font-semibold transition-all">
                    Hủy
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUser } from '../../store/user.store';
const userStore = useUser()
import { update_user } from '../../services/app.service';
import { useWellness } from '../../store/wellness.store';
const wellnessStore = useWellness()
import { X } from 'lucide-vue-next';
// Profile State

const userProfile = computed(() => ({
    weight: userStore.user?.weight || 0,
    height: userStore.user?.height || 0,
    target_weight: userStore.user?.target_weight || 0,
    day_of_birth: userStore.user?.day_of_birth || '1990-01-01',
    BMI: userStore.user?.BMI || 0,
    dailyCalorieGoal: wellnessStore.dailyNutrition?.calories_target || 2000,
    typeBMI: userStore.user?.type_BMI || 'Unknown',
    sex: userStore.user?.sex || 'M',
    activity_level: userStore.user?.activity_level || 'sedentary',
    goal: userStore.user?.goal || 'maintain',
    date: wellnessStore.dailyNutrition?.date,
}))
const editProfileData = computed(() => ({ ...userProfile.value }));
const showProfileModal = ref(false);
const ShowFilterModal = ref(false)
// Meals Data
const mealCategories = ['tất cả', 'breakfast', 'lunch', 'dinner', 'snacks', 'vegetables', 'fruits', 'lean_protein', 'whole_grains', 'dairy', 'nuts'];
const selectedCategory = ref('tất cả');
const isHealthy = ref(false);
const menus = ref(null)
const foods = ref([])

const selectedMeals = ref([]);
const filteredMeals = computed(() => {
    return foods.value.filter(meal => meal.category.toLowerCase() === selectedCategory.value.toLowerCase());
});
// Computed Properties
const filterFoodItems = computed(() => {
    if (selectedCategory.value === 'tất cả') return wellnessStore.listFoodItems;
    currentPage.value = 1; // Reset về trang đầu khi đổi category
    return wellnessStore.listFoodItems.filter(item => item.category === selectedCategory.value);
});
const calculateTotalNutrition = () => {
    return selectedMeals.value.reduce((total, meal) => {
        return {
            calories: total.calories + meal.calories,
            protein: total.protein + meal.protein,
            carbs: total.carbs + meal.carbs,
            fat: total.fat + meal.fat
        };
    }, { calories: 0, protein: 0, carbs: 0, fat: 0 });
};

// Methods
const addMealToDay = (meal) => {
    if (!selectedMeals.value.some(m => m.id === meal.id)) {
        selectedMeals.value.push({ ...meal });
    }
};

const removeMealFromDay = (idx) => {
    selectedMeals.value.splice(idx, 1);
};

const saveProfile = async () => {
    console.log('Saving Profile with data:', editProfileData.value);
    await update_user(editProfileData.value);
    showProfileModal.value = false;
    await userStore.fetchUser()  // Refresh user data after update
    await wellnessStore.fetchDailyNutrition(userStore.user?.id, new Date().toISOString().split('T')[0])  // Refresh nutrition data
};

// Logic đơn giản trong Script
const itemsPerPage = filterFoodItems.value.length > 0 ? 8 : 0; // Số lượng mục hiển thị mỗi trang, có thể điều chỉnh tùy theo nhu cầu
const currentPage = ref(1);
const page = computed(() => {
    return Math.ceil(filterFoodItems.value.length / itemsPerPage);
});
const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filterFoodItems.value.slice(start, end);
});

// Giả sử data của bạn nằm trong biến 'recommend_menu'
const get_menu_handle = async () => {
    await wellnessStore.fetchDailyMenu(userStore.user.id)
    menus.value = wellnessStore.dailyMenu
};
const recommend_menu = computed(() => ({
    breakfast: menus.value?.breakfast || [],
    lunch: menus.value?.lunch || [],
    dinner: menus.value?.dinner || [],
    snacks: menus.value?.snacks || [],
    total_calories: menus.value?.total_calories || 0,
    total_protein: menus.value?.total_protein || 0,
    total_carbs: menus.value?.total_carbs || 0,
    total_fat: menus.value?.total_fat || 0,
}));

const selectedBuoi = ref('all');
// 1. Xóa món
const removeFood = (mealType, index) => {
    recommend_menu.value[mealType].splice(index, 1);
    updateTotals(); // Hàm tính lại tổng calories, protein...
};

// 2. Đổi 1 món đơn lẻ (Remake)
const remakeSingleFood = async (mealType, index) => {
    // Lấy một món ngẫu nhiên từ danh sách gốc (listFoodItems) cùng category
    const pool = wellnessStore.listFoodItems.filter(f => f.category === mealType);
    if (pool.length > 0) {
        const randomFood = pool[Math.floor(Math.random() * pool.length)];
        recommend_menu.value[mealType][index] = { ...randomFood };
        updateTotals();
    }
};

// 3. Thêm món mới
const currentAddingMealType = ref(null);
const showAddFoodModal = ref(false);
const addNewFood = (food) => {
    // Implementation for adding new food
    if (currentAddingMealType.value) {
        recommend_menu.value[currentAddingMealType.value].push({ ...food });
        updateTotals();
    }
};

const addNewFoodHandle = (mealType) => {
    showAddFoodModal.value = true;
    currentAddingMealType.value = mealType;
    console.log('Thêm món mới cho:', mealType);
    console.log('Danh sách món hiện tại:', recommend_menu.value[mealType]);

};

// 4. Hàm cập nhật lại con số tổng ở Header
const updateTotals = () => {
    let cal = 0, pro = 0, carb = 0, fat = 0;
    ['breakfast', 'lunch', 'dinner', 'snacks'].forEach(type => {
        recommend_menu.value[type].forEach(food => {
            cal += food.calories;
            pro += food.protein;
            carb += food.carbs;
            fat += food.fat;
        });
    });
    recommend_menu.value.total_calories = Math.round(cal);
    recommend_menu.value.total_protein = Math.round(pro * 10) / 10;
    recommend_menu.value.total_carbs = Math.round(carb * 10) / 10;
    recommend_menu.value.total_fat = Math.round(fat * 10) / 10
};
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
}
</style>
