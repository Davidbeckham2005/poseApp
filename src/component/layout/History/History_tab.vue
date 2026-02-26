<template>
    <div>
        <Title_content title="Analysis History" content="View past workout sessions and progress"></Title_content>
        <div class="sm:flex space-x-5 mb-5">
            <History_box v-for="(item, key) in items" :key="key" :item="item">
            </History_box>
        </div>
        <!-- <button class="btn btn-outline" @click="delete_select">Delete</button> -->
        <div class="space-y-4">
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Showing {{ videoStore.total_video }} of {{ videoStore.total_video }}
                    Sessions</span>
                <span class="text-cyan-400" @click="select_all">Select all</span>
            </div>
            <History_item_video v-for="video in videoStore.videos" :video="video" @select_video="append_on_delete_list"
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
import { Video, CircleCheckBig, Shell, ChartNoAxesCombined, Trophy, List } from 'lucide-vue-next';
import { ref, watch } from 'vue';
const List_Video = ref([])
const append_on_delete_list = (path) => {
    const index = List_Video.value.indexOf(path)
    if (index === -1) {
        List_Video.value.push(path)
    } else {
        List_Video.value.splice(index, 1)
    }
}

const items = {
    video: { icon: Video, first_line: 'Total Sessions', middle_value: '12', last_line: '8 this week', color_icon: 'text-cyan-400', green_line: "" },
    video2: { icon: CircleCheckBig, first_line: 'Completed', middle_value: '12', last_line: '83% success rate', color_icon: 'text-green-400', green_line: "text-green-400" },
    video3: { icon: Shell, first_line: 'Avg Accuracy', middle_value: '22%', last_line: '+5% last week', color_icon: 'text-purple-400', green_line: "text-green-400" },
    video4: { icon: ChartNoAxesCombined, first_line: 'Total Reps', middle_value: '12', last_line: 'Across all workouts', color_icon: 'text-blue-400', green_line: "" },
    video5: { icon: Trophy, first_line: 'Best Score', middle_value: '12%', last_line: 'Personal record', color_icon: 'text-yellow-400', green_line: "" },
}
// xoa duoc chon
const select_all = () => {
    if (List_Video.value.length === videoStore.videos.length) {
        List_Video.value = []
    } else {
        List_Video.value = videoStore.videos.map(v => v.output_path)
    }
    // console.log(List_Video.value)
}
const delete_select = () => {
    const data = {
        "output_paths": List_Video.value
    }
    videoStore.delete_videos_store(data)
    List_Video.value = []
}
</script>
