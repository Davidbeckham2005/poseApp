<template>
    <div class="w-full rounded-full h-3">
        <div :class="['h-2 bg-cyan-500 rounded-full shadow-sm transition-all duration-700']"
            :style="{ width: progress + '%' }"></div>
        <div class="flex justify-between">
            <span class="text-sm text-gray-400">Progressing</span>
            <span class="text-cyan-400 text-sm">{{ progress }}%</span>
        </div>
        <div class="mt-2 space-y-2  p-2 bg-gray-800/50 border border-slate-800 shadow-2xl rounded-2xl">
            <cp_task_running text="Uploading video" :color="progress > 10 ? 'text-green-400' : ' '" :icon="CircleCheck"
                :animate="progress < 10 ? 'animate-spin' : ''">

            </cp_task_running>
            <cp_task_running text=" Analyzing frames" :color="progress > 40 ? 'text-cyan-400' : ''" :icon="Brain"
                :animate="progress < 40 && progress > 10 ? 'animate-spin' : ''">
            </cp_task_running>
            <cp_task_running text="Import mediapipe solutions" :color="progress > 86 ? 'text-cyan-400' : ''"
                :icon="BotMessageSquare" :animate="progress > 40 && progress < 86 ? 'animate-spin' : ''">
            </cp_task_running>
            <cp_task_running text="Finishing" :color="progress >= 99 ? 'text-green-400' : ''" :icon="BugOff"
                :animate="progress >= 86 ? 'animate-spin' : ''">
            </cp_task_running>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    isLoading: Boolean,
})

import { computed, onMounted, ref, watch } from 'vue';
import cp_task_running from '../bases/cp_task_running.vue';
import { CircleCheck, Brain, BugOff, BotMessageSquare, Bot } from 'lucide-vue-next'


const progress = ref(0)
const speed_progress = ref(100)

watch(progress, (newVal) => {
    if (progress.value >= 95) {
        speed_progress.value = 2000
    }
    else if (progress.value > 70) {
        speed_progress.value = 500
    } else if (progress.value > 40) {
        {
            speed_progress.value = 300
        }
    }
})

const startLoading = () => {

    if (progress.value <= 97)
        setTimeout(() => {
            progress.value += 1
            startLoading()
        }, speed_progress.value)

    else {
        setTimeout(() => {
            progress.value += 1
        }, 2000)
    }
}

startLoading()
// watch(() => props.isLoading, (newVal) => {
//     if (newVal == false) {
//         clearInterval(interval)
//         progress.value = 100

//     }
// })

</script>

<style lang="scss" scoped></style>