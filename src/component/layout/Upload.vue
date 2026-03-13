<script setup>
// khai bao cac component
import title_content from "../bases/title_content.vue";
import VideoResult from "./VideoResult.vue";
import Load_progres from "./Load_progres.vue";
import cp_Load from "../bases/cp_Load.vue";
import { useNavigation, get_translate, get_status_upload_video } from "../../composable/helpers";
import { ref } from 'vue'
import Exercise_card from './Upload/Exercise_card.vue'
import { exercises_data } from "../../constants/exercise";
import ExerciseGuideModal from './Upload/ExerciseGuideModal.vue';
import { useUpload } from "../../composable/upload";

const { time_video_upload, src_video } = useUpload()
const exercises = ref(exercises_data)
const isloading = get_status_upload_video()
const isGuideOpen = ref(false);
const selectedExercise = ref(null);

const openGuide = (exercise) => {
    selectedExercise.value = exercise;
    isGuideOpen.value = true;
};

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
            class="min-h-screen dark:bg-[#0a0a0c] p-12 text-gray-200 font-sans selection:bg-orange-500 selection:text-white">
            <div class="max-w-7xl mx-auto space-y-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <Exercise_card @click.prevent="openGuide(exercise)" v-for="exercise in exercises"
                        :key="exercise.title" v-bind="exercise" />
                </div>
                <ExerciseGuideModal :isOpen="isGuideOpen" :exercise="selectedExercise" @close="isGuideOpen = false" />
            </div>
        </div>
    </div>
</template>