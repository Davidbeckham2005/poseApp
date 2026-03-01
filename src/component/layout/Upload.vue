<script setup>
// khai bao veevalidate
import { Form, Field } from 'vee-validate'
// khai bao cac component
import title_content from "../bases/title_content.vue";
import VideoResult from "./VideoResult.vue";
import Load_progres from "./Load_progres.vue";
import History from "./History/History.vue";
import cp_Load from "../bases/cp_Load.vue";
// khai bao api add video
import { addVideo } from "../../services/app.service";

import { open } from "@tauri-apps/plugin-dialog";

// khai bao cac ham dung chung
import { useNavigation, get_translate, get_status_upload_video } from "../../composable/helpers";
const { switch_dashbroad } = useNavigation()

// cac ham ho tro tu he thong
import { onMounted, ref } from "vue";
import { convertFileSrc } from "@tauri-apps/api/core";

// khai bao pinia
import { useVideo } from "../../store/video.store";
const videoStore = useVideo()
import { useSetting } from "../../store/setting.store";
const settingStore = useSetting()
// khai bao bien
const src_video = ref()
const isloading = get_status_upload_video()
const translate_class = get_translate()
// list cac bai tap 
const exercises = [
    { name: 'Squat', value: 'squat' },
    { name: 'Push-up', value: 'pushup' },
    { name: 'Plank', value: 'plank' },
]
// api 
import { get_tinme_video } from '../../services/app.service';
// const select_type = ref(true)
const exercise_selected = ref()
// const emit = defineEmits(['analying'])
import video_wait from "../bases/video_wait.vue";
const time_video_upload = ref()
async function upload() {
    if (!exercise_selected.value) {
        // select_type.value = false
        // alert("Please choose a exercise type first!")
        return
    }
    try {
        console.log(exercise_selected.value)
        const pathSelected = await open({
            filters: [{
                name: "video",
                extensions: ["mp4", "avi"]
            }]
        })

        if (pathSelected) {
            src_video.value = convertFileSrc(pathSelected)
            const encodePath = encodeURIComponent(pathSelected)
            const data = {
                "path_video": encodePath,
                "type": exercise_selected.value,
                "isDrawing": settingStore.setting.isDrawing,
                "isAnalyst": settingStore.setting.isAnalyst,
                "isCheck_view": settingStore.setting.isCheck_view,
                "Analyst_FPS": settingStore.setting.Analyst_FPS,
                "Analyst_count": settingStore.setting.Analyst_count,
                "Analyst_count_good": settingStore.setting.Analyst_count_good,
                "Analyst_estimate": settingStore.setting.Analyst_estimate,
                "Analyst_state": settingStore.setting.Analyst_state,
            }
            const data_to_get_time_video = {
                "path": encodePath
            }
            isloading.value = true
            time_video_upload.value = await get_tinme_video(data_to_get_time_video)
            console.log(time_video_upload.value)
            const res = await addVideo(data)
            while (true) {
                await videoStore.fetchVideo()
                // const all_video = await get_all_video()
                // console.log(res.output_path, all_video)
                // console.log(res.output_path, videoStore.videos)
                if (videoStore.get_video(res.output_path)) break
                await new Promise(r => setTimeout(r, 500))
            }
            switch_dashbroad(res.output_path)
        }
    }
    catch (error) {
        console.log(error)
    } finally {
        isloading.value = false
    }
}
import { VideoIcon, UploadCloud } from 'lucide-vue-next';
const value_video_wait = {
    title: "Drop video file here",
    content: "Drag and drop your exercise videos here, or click to browse",
    main_icon: UploadCloud,
    small_icon: VideoIcon,
    small_text: "MP4, AVI - Max 500MB",
}
</script>
<template>
    <Transition v-bind="translate_class">
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
            <title_content title="Upload Video"
                content="Upload your exercise video for automated pose detection and analysis"></title_content>
            <div class="rounded-2xl bg-gray-700/60 p-3 mb-5 h-40">
                <title_content title="Exercise Type" content="Pre-select exercise for optimized detection" class="ml-2">
                </title_content>
                <Field name="type" as="select" v-model="exercise_selected"
                    :class="['w-full rounded-2xl bg-gray-700/80 h-10 pl-2 pr-2 border border-red-400 hover:border hover:border-cyan-400', { 'border-red-400': !exercise_selected, 'border-0': exercise_selected }]">
                    <option value="" disabled class="text-white">-- Select Exercise --</option>
                    <option v-for="exercise in exercises" :value="exercise.value" class="group">{{
                        exercise.name }}</option>
                </Field>
            </div>
            <video_wait v-bind="value_video_wait" @click.prevent="upload"></video_wait>
            <History></History>
        </div>
    </Transition>
</template>