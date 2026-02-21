<script setup>
import Analyst_status from '../Analyst/Analyst_status.vue'
import Analyst_name from '../Analyst/Analyst_name.vue';
import Activity_log from '../Analyst/Activity_log.vue';
import title_content from '../bases/title_content.vue';
import square_shape from '../bases/square_shape.vue';
import {
    Shell,
    CircleCheckBig,
} from 'lucide-vue-next'
const props = defineProps({
    reps_count: {
        type: String,
        default: "0"
    },
    accuracy: String,
    video_record: Array,
})

const colorMap = {
    high: "text-orange-400",
    good: 'text-green-400',
    bad: 'text-red-400'
}
</script>

<template>
    <div class="md:pl-2 space-y-6">
        <title_content title="Analysis" content="Performance metrics and feedback"></title_content>
        <!-- <Analyst_status status="Detecting Pose . . ."></Analyst_status> -->
        <Analyst_name exercise="Squat"></Analyst_name>
        <div class="flex flex-row space-x-5 justify-center">
            <square_shape :icon=Shell type="Reps count" :value="reps_count" text_color='text-green-500'></square_shape>
            <square_shape :icon=CircleCheckBig type="Good" :value="accuracy" text_color="text-blue-500">
            </square_shape>
        </div>
        <div class="bg-gray-700/50 p-3 rounded-2xl font-semibold space-y-4">
            <p class="text-gray-500 mb-4 text-sm border-b pb-2 border-gray-700/30">Activity log</p>
            <Activity_log v-for="record in video_record" :count="record.count" :require="record.require"
                :color="colorMap[record.estimate]">
            </Activity_log>
        </div>
    </div>
</template>