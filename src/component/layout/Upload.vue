<script setup>
// khai bao cac component
import title_content from "../bases/title_content.vue";
import VideoResult from "./VideoResult.vue";
import Load_progres from "./Load_progres.vue";
import cp_Load from "../bases/cp_Load.vue";
import { useNavigation, get_translate, get_status_upload_video } from "../../composable/helpers";
import { ref, computed } from 'vue'
import Exercise_card from './Upload/Exercise_card.vue'
import { useExercise } from "../../constants/exercise";
const { get_exercises } = useExercise()
import ExerciseGuideModal from './Upload/ExerciseGuideModal.vue';
import { useUpload } from "../../composable/upload";

const { time_video_upload, src_video } = useUpload()
const exercises = get_exercises()
const isloading = get_status_upload_video()
const isGuideOpen = ref(false);
const selectedExercise = ref(null);

const openGuide = (exercise) => {
    selectedExercise.value = exercise;
    isGuideOpen.value = true;
};
// vibe code
// Lấy danh sách tất cả các nhóm cơ duy nhất từ exercises_data
const allMuscles = computed(() => {
    console.log('Exercises data:', exercises);
    const muscles = new Set();
    exercises.forEach(ex => {
        ex.muscles.forEach(m => muscles.add(m));
    });
    // Trả về mảng đã sắp xếp theo bảng chữ cái
    return Array.from(muscles).sort();
});
const searchQuery = ref('');
const selectedMuscle = ref('All');
const selectedDifficulty = ref('All');
const equipmentFilter = ref('all'); // 'all', 'equipment', 'bodyweight'
const filteredExercises = computed(() => {
    return exercises.filter(ex => {
        const matchSearch = ex.title.toLowerCase().includes(searchQuery.value.toLowerCase());
        // 1. Lọc theo nhóm cơ (nằm trong mảng muscles)
        const matchMuscle = selectedMuscle.value === 'All' ||
            ex.muscles.includes(selectedMuscle.value);

        // 2. Lọc theo độ khó
        const matchDifficulty = selectedDifficulty.value === 'All' ||
            ex.difficulty === selectedDifficulty.value;

        // 3. Lọc theo dụng cụ
        const matchEquipment = equipmentFilter.value === 'all' ||
            (equipmentFilter.value === 'equipment' ? ex.hasEquipment : !ex.hasEquipment);

        return matchMuscle && matchDifficulty && matchEquipment && matchSearch;
    });
});

</script>
<template>

    <div v-if="isloading" class="flex flex-col items-center animate-fade-in duration-1000 pb-3">
        <cp_Load speed="3s"></cp_Load>
        <VideoResult :path_video="src_video" title="Review" content="Review your video first!" size_video="w-80"
            :is-controls="true" :isloop="true" class="m-auto"
            text_video="Please do not switch tabs during the detection!">
        </VideoResult>
        <div class="w-120 h-4 pt-2">
            <Load_progres :is-loading="isloading" :time_loading="time_video_upload" class=""></Load_progres>
        </div>
    </div>
    <div v-else>
        <title_content title="Tải video lên" content="Tải lên video của bạn để tiến hành phân tích">
        </title_content>
        <div
            class="min-h-screen dark:bg-[#0a0a0c] text-gray-200 font-sans selection:bg-orange-500 selection:text-white">
            <div class="max-w-7xl mx-auto space-y-10">
                <div
                    class="grid grid-cols-1 lg:grid-cols-5 gap-4 items-center p-5 rounded-2xl shadow-sm border border-slate-200">

                    <div class="relative lg:col-span-2">
                        <input v-model="searchQuery" type="text" placeholder="Tìm tên bài tập..."
                            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 p-2.5 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none text-sm font-semibold text-slate-700 transition-all cursor-pointer" />
                    </div>

                    <div class="grid grid-cols-2 lg:col-span-3 space-x-2 h-full">
                        <div class="flex flex-row grid-span-1 space-x-2"><select v-model="selectedMuscle"
                                class="w-full bg-slate-50 p-2.5 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none text-sm font-semibold text-slate-700 transition-all cursor-pointer">
                                <option value="All">Tất cả nhóm cơ</option>
                                <option v-for="muscle in allMuscles" :key="muscle" :value="muscle">
                                    {{ muscle }}
                                </option>
                            </select>
                            <select v-model="selectedDifficulty"
                                class="w-full bg-slate-50 p-2.5 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none text-sm font-semibold text-slate-700 transition-all cursor-pointer">
                                <option value="All">Mọi cấp độ</option>
                                <option value="Beginner">Beginner</option>
                                <option value="Intermediate">Intermediate</option>
                                <option value="Advanced">Advanced</option>
                            </select>
                        </div>
                        <div class="flex rounded-xl p-1 border ">
                            <button @click="equipmentFilter = 'all'"
                                :class="equipmentFilter === 'all' ? ' text-blue-600' : 'text-slate-500'"
                                class="flex-1 py-1.5 rounded-lg transition-all text-xs font-bold uppercase">Tất
                                cả</button>
                            <button @click="equipmentFilter = 'bodyweight'"
                                :class="equipmentFilter === 'bodyweight' ? ' text-blue-600' : 'text-slate-500'"
                                class="flex-1 py-1.5 rounded-lg transition-all text-xs font-bold uppercase">Body</button>
                            <button @click="equipmentFilter = 'equipment'"
                                :class="equipmentFilter === 'equipment' ? ' text-blue-600' : 'text-slate-500'"
                                class="flex-1 py-1.5 rounded-lg transition-all text-xs font-bold uppercase">Có
                                tạ</button>
                        </div>
                    </div>


                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <Exercise_card @click.prevent="openGuide(exercise)" v-for="exercise in filteredExercises"
                        :key="exercise.title" v-bind="exercise" />
                </div>
                <ExerciseGuideModal :isOpen="isGuideOpen" :exercise="selectedExercise" @close="isGuideOpen = false" />
            </div>
        </div>
    </div>
</template>