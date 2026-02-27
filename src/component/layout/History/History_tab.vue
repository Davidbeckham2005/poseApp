<template>
    <div>
        <Title_content title="Analysis History" content="View past workout sessions and progress"></Title_content>
        <div class="sm:flex space-x-5 mb-5">
            <History_box v-for="(item, key) in items" :key="key" :item="item">
            </History_box>
        </div>
        <div class="flex space-x-3 relative">
            <div class="relative w-full">
                <Search class="absolute mt-3 ml-3"></Search>
                <input placeholder="Search by exercise name" type="text" class="block w-full pl-12 pr-4 py-3 bg-gray-700/50 border border-white/20 rounded-xl
            text-gray-300 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-cyan-400 focus:border-cyan-400
            transition-all" v-model="data_search">
            </div>
            <div @click="isshow_filter = !isshow_filter"
                :class="['w-34 pl-4 pr-4  border border-white/20 rounded-xl text-gray-300 flex py-3 gap-2 justify-center-safe', { 'bg-cyan-400/75': isshow_filter, 'bg-gray-700/50': !isshow_filter }]">
                <Funnel></Funnel> <span>Filters</span>
            </div>
        </div>
        <div v-if="isshow_filter"
            class="bg-gray-700/50 border border-white/20 w-full mt-4 h-25 rounded-2xl flex items-center pl-4">
            <div class="w-44 h-15 space-y-3 flex flex-col justify-between">
                <span class="text-gray-500 text-sm">Sort By</span>
                <Field name="sort" as="select" v-model="sort_selected"
                    class="text-white w-full rounded-lg bg-gray-900/90 h-15 pl-2 pr-2 p-2 border border-white/20 focus:border-cyan-400">
                    <option value=" " disabled>--Select--</option>
                    <option :value="key" v-for="(sort, key) in sorts" :key="key" @change="sort.value = true">{{
                        key }}</option>
                </Field>
            </div>
        </div>

        <!-- <button class="btn btn-outline" @click="delete_select">Delete</button> -->
        <div class="space-y-4 mt-2">
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Showing {{ videos.length }} of {{ videoStore.total_video }}
                    Sessions</span>
                <span class="text-cyan-400" @click="select_all">Select all</span>
            </div>
            <History_item_video v-for="video in videos" :video="video" @select_video="append_on_delete_list"
                :is-selected="List_Video.includes(video.output_path)">
            </History_item_video>
        </div>
    </div>
</template>

<script setup>
// componnt
import Title_content from '../../bases/title_content.vue';
import History_box from './History_box.vue';
import History_item_video from './History_item_video.vue';
import { useVideo } from '../../../store/video.store';
const videoStore = useVideo()
import { Video, CircleCheckBig, Shell, Search, ChartNoAxesCombined, Trophy, Funnel } from 'lucide-vue-next';
import { computed, ref, watch } from 'vue';
// veevalidate
import { Field } from 'vee-validate';
const sort_selected = ref("")
const List_Video = ref([])
const append_on_delete_list = (path) => {
    const index = List_Video.value.indexOf(path)
    if (index === -1) {
        List_Video.value.push(path)
    } else {
        List_Video.value.splice(index, 1)
    }
}
const sorts = {
    Date: { value: false },
    Reps: { value: false },
    Accuracy: { value: false },
}
const items = {
    video: { icon: Video, first_line: 'Total Sessions', middle_value: '12', last_line: '8 this week', color_icon: 'text-cyan-400', green_line: "" },
    video2: { icon: CircleCheckBig, first_line: 'Completed', middle_value: '12', last_line: '83% success rate', color_icon: 'text-green-400', green_line: "text-green-400" },
    video3: { icon: Shell, first_line: 'Avg Accuracy', middle_value: '22%', last_line: '+5% last week', color_icon: 'text-purple-400', green_line: "text-green-400" },
    video4: { icon: ChartNoAxesCombined, first_line: 'Total Reps', middle_value: '12', last_line: 'Across all workouts', color_icon: 'text-blue-400', green_line: "" },
    video5: { icon: Trophy, first_line: 'Best Score', middle_value: '12%', last_line: 'Personal record', color_icon: 'text-yellow-400', green_line: "" },
}
// filter
const isshow_filter = ref(false)















// xoa duoc chon
const select_all = () => {
    if (List_Video.value.length === videoStore.videos.length) {
        List_Video.value = []
    } else {
        List_Video.value = videoStore.videos.map(v => v.output_path)
    }
    // console.log(List_Video.value)
}
const data_search = ref()
const videos = computed(() => {
    if (data_search.value) {
        return videoStore.videos.filter(v => v.type.includes(data_search.value.toLowerCase()))
    }
    return videoStore.videos
})
const delete_select = () => {
    const data = {
        "output_paths": List_Video.value
    }
    videoStore.delete_videos_store(data)
    List_Video.value = []
}
</script>
