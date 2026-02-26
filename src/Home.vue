<template>
    <div class="flex h-screen bg-[#0a0a0c] text-gray-300 font-sans">
        <sidebar class="w-36 md:w-70 border-r border-gray-800 flex flex-col" :menu-items="menuItems"
            :current-tab="currentTab" @active-menu="setActive">
        </sidebar>
        <main class="flex-1 flex flex-col overflow-y-auto">
            <Header class="flex items-center justify-between px-6 py-4 border-b border-gray-800"></Header>
            <div class="py-4 px-4 max-w-6xl mx-auto w-full ">
                <div v-if="currentTab === `dashboard`" class="flex flex-col sm:flex-row">
                    <VideoResult class="w-full lg:w-3/4" title="Live Analysis" :path_video="video_src"
                        content="Real-time pose detection and form tracking"></VideoResult>
                    <Analyst v-bind="Analysis_value" class="sm:ml-4 w-full lg:w-1/4"></Analyst>
                </div>
                <Upload v-else-if="currentTab === `upload`"></Upload>
                <Settings v-else-if="currentTab === `settings`">
                </Settings>
                <History_tab v-else-if="currentTab === `history`">

                </History_tab>
                <!-- <div class="grid grid-cols-3 gap-6">
                    <div v-for="i in 3" :key="i"
                        class="bg-gray-900/40 border border-gray-800 p-5 rounded-xl hover:border-gray-700 transition cursor-pointer">
                        <div class="bg-gray-800 w-10 h-10 rounded flex items-center justify-center mb-4">
                            <VideoIcon class="w-5 h-5 text-gray-400" />
                        </div>
                        <h4 class="font-medium text-white">Sample Video {{ i }}</h4>
                        <p class="text-sm text-gray-500 mt-1">{{ ['Squat Exercise', 'Push-up Demo', 'Plank Hold'][i
                            - 1]
                        }}</p>
                    </div>
                </div>
                <div class="bg-gray-900/20 border border-gray-800 rounded-xl p-6">
                    <h4 class="font-semibold text-white mb-4">Upload Guidelines</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                            Ensure the subject is clearly visible in the frame</li>
                        <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                            Good lighting improves pose detection accuracy</li>
                        <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                            Avoid cluttered backgrounds for best results</li>
                        <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                            Supported exercises: squat, push-up, plank, lunge, etc.</li>
                    </ul>
                </div> -->
            </div>

        </main>
    </div>
</template>

<script setup>
import {
    LayoutDashboardIcon as DashboardIcon,
    ActivityIcon as AnalysisIcon,
    HistoryIcon,
    SettingsIcon,
    PlayCircleIcon as PlayIcon,
    UploadIcon,

} from 'lucide-vue-next';
// component
import Analyst from "./component/layout/Analyst.vue";
import Header from './component/layout/Header.vue';
import sidebar from './component/layout/sidebar/sidebar.vue';
import Upload from './component/layout/Upload.vue';
import VideoResult from './component/layout/VideoResult.vue';
import Settings from './component/layout/Settings.vue';
import History_tab from './component/layout/History/History_tab.vue';

import { watch, ref, computed, onMounted } from "vue";
import { useNavigation } from "./composable/helpers";
const { switch_on_sidebar, currentTab, currentFile } = useNavigation()

//pinia 
import { useSetting } from './store/setting.store';
import { useVideo } from './store/video.store';
const videoStore = useVideo()
const settingStore = useSetting()

// onMounted(async () => {
//     await settingStore.fetchSetting()
//     console.log(settingStore.setting)
// })
const menuItems = [
    { name: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
    { name: 'upload', label: 'Upload', icon: UploadIcon },
    // { name: 'analysis', label: 'Analysis', icon: AnalysisIcon },
    { name: 'history', label: 'History', icon: HistoryIcon },
    { name: 'settings', label: 'Settings', icon: SettingsIcon },

];

switch_on_sidebar("upload")
// thay doi cac tab
const setActive = (item) => {
    switch_on_sidebar(item.name)
    // console.log(currentTab.value)
}


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
// ta quan sat current file chu khong the quan sat current file . value boi vi 
// 1. vi no phai la gia tri thay doi neu . value thi ko thay doi duoc => sai 
// 2. sao khi fetch muon dung du lieu tuyet doi phai dung async - await
// 3. có thể spam fetch
watch(currentFile, async () => {
    await videoStore.fetchVideo()
    // console.log(currentFile.value, videoStore.videos)
    // const result = videoStore.videos.find(v => v.output_path == currentFile.value)
    // console.log(result)
    // const video = videoStore.get_video(currentFile)
    // const res = await get_video(currentFile.value)
    // console.log(currentFile.value, res)
    // video_src.value = `../src/assets/videos/${currentFile.value}.mp4`;
}, { immediate: true })

// ======> viec hien thi result phu thuoc vao ham currenfile => tu ham switch_dashboard(path)
const video = computed(() => {
    return videoStore.get_video(currentFile.value)
})
const video_src = computed(() => {
    return `../src/assets/videos/${currentFile.value}.mp4`;
})
// du lieu ta co o pinia khong kip thoi de nhan nen phai call api lay truc tiep tu database 
</script>