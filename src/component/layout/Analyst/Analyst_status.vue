<template>
    <div class="grid grid-cols-4 gap-4 items-center rounded-2xl bg-gray-700/50 p-2 h-20 w-full pl-5">
        <component :is="status === 'Ready' ? Clock : AnalysisIcon"
            :class="['w-12 h-12 col-span-1 rounded-lg bg-zinc-700 p-2', status === 'Ready' ? 'text-white/40' : 'text-cyan-400']">
        </component>
        <div class="col-span-3">
            <h1 class="text-sm text-zinc-400">Status</h1>
            <p class="text-sm font-semibold text-white">{{ status }}</p>
        </div>
    </div>
</template>

<script setup>
import {
    ActivityIcon as AnalysisIcon,
    Clock
} from 'lucide-vue-next'
defineProps({
    status: String
})
</script>

<style lang="scss" scoped></style>