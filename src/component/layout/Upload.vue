<script setup>
import {
    UploadCloud,
    VideoIcon
} from "lucide-vue-next"


// khai bao cac component
import title_content from "../bases/title_content.vue";
import VideoResult from "./VideoResult.vue";
import Load_progres from "./Load_progres.vue";
import History from "./History/History.vue";
import cp_Load from "../bases/cp_Load.vue";
import Title_content_horizontal from "../bases/Title_content_horizontal.vue";
// khai bao api add video
import { addVideo, get_video, get_all_video } from "../../services/app.service";

import { open } from "@tauri-apps/plugin-dialog";

// khai bao cac ham dung chung
import { useNavigation, get_translate, get_status_upload_video } from "../../composable/helpers";
const { switch_on_sidebar, currentTab, switch_dashbroad, currentFile } = useNavigation()

// cac ham ho tro tu he thong
import { onMounted, ref } from "vue";
import { convertFileSrc } from "@tauri-apps/api/core";

// khai bao pinia
import { useVideo } from "../../store/video.store";
const videoStore = useVideo()

// khai bao bien
const src_video = ref()
const isloading = get_status_upload_video()
const translate_class = get_translate()

const emit = defineEmits(['analying'])
async function upload() {
    try {
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
            }
            isloading.value = true
            const res = await addVideo(data)
            while (true) {
                await videoStore.fetchVideo()
                const all_video = await get_all_video()
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

</script>
<template>
    <Transition v-bind="translate_class">
        <div v-if="isloading" class="flex flex-col items-center animate-fade-in duration-1000 p-2 pb-3">
            <cp_Load speed="3s"></cp_Load>
            <VideoResult :path_video="src_video" title="Review" content="Review your video first!" size_video="w-80"
                :is-controls="false" :isloop="true" class="m-auto"
                text_video="Please do not switch tabs during the detection!">
            </VideoResult>
            <div class="w-120 h-4 pt-2">
                <Load_progres :is-loading="isloading" class=""></Load_progres>
            </div>
        </div>
        <div v-else>
            <title_content title="Upload Video"
                content="Upload your exercise video for automated pose detection and analysis"></title_content>
            <div class="rounded-2xl bg-gray-700/50 p-3 mb-5 h-30 space-y-5">

                <!-- <Label for="type"></Label>
                <Field name="type" as="select">
                    <option value="squat">squat</option>
                </Field> -->
            </div>
            <div @click.prevent="upload" class="max-w-6xl border-2 border-dashed border-gray-700 rounded-2xl
        bg-stone-900/70 p-10 sm:p-20 flex flex-col items-center justify-center text-center cursor-pointer
        hover:border-cyan-400/60 transition group">
                <div
                    class="hidden md:w-30 md:h-30 bg-gray-800 rounded-full sm:flex items-center justify-center mb-6 group-hover:scale-110 transition">
                    <UploadCloud class="text-cyan-400 w-8 h-8" />
                </div>
                <title_content title="Drop video file here"
                    content="Drag and drop your exercise videos here, or click to browse"></title_content>
                <div class="flex items-center sm:space-x-4 text-xs text-gray-600">
                    <VideoIcon class="w-4 h-4 mr-1" /> MP4, AVI - Max 500MB
                </div>
            </div>
            <History></History>
        </div>
    </Transition>
</template>