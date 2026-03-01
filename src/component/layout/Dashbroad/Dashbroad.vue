<template>
    <div class="flex flex-col sm:flex-row">
        <VideoResult v-if="currentFile" class="w-full lg:w-3/4" title="Live Analysis" :path_video="video_src"
            content="Real-time pose detection and form tracking"></VideoResult>
        <video_wait v-bind="value_video_wait" v-else class="w-full"></video_wait>
        <Analyst v-bind="Analysis_value" class="sm:ml-4 w-full lg:w-1/4"></Analyst>
    </div>
</template>

<script setup>
import { useNavigation } from '../../../composable/helpers';
const { currentFile } = useNavigation()
import VideoResult from '../VideoResult.vue';
import video_wait from '../../bases/video_wait.vue';
import { computed } from 'vue';
import Analyst from '../Analyst/Analyst.vue';
// pinia
import { useVideo } from '../../../store/video.store';
const videoStore = useVideo()

const video_src = computed(() => {
    return `../src/assets/videos/${currentFile.value}.mp4`;
})
const video = computed(() => {
    return videoStore.get_video(currentFile.value)
})
const Analysis_value = computed(() => {
    if (video.value) {
        let count = " reps"
        if (video.value.type == 'plank') count = ' sec'
        return {
            reps_count: video.value.total + count,
            accuracy: video.value.accuracy_good + "%",
            video_record: video.value.record_detail,
            type: video.value.type
        }
    }
    return {
        reps_count: "...",
        accuracy: "...",
        type: "..."
    }
})
import { Play, VideoIcon } from 'lucide-vue-next';
const value_video_wait = {
    title: "No video loaded",
    content: "Upload a video to start analysis",
    main_icon: Play,
    small_icon: VideoIcon,
    small_text: "MP4, AVI - Max 500MB",
}
</script>
