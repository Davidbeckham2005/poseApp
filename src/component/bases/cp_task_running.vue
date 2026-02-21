<template>
    <div :class="['flex flex-row justify-between p-2', color]">
        <div class="flex flex-row space-x-2">
            <div class="p-2 bg-gray-600/20 rounded-sm">
                <component :is="icon" class="h-7 w-7 inline-block"></component>
            </div>
            <p class="mt-2 text-md font-semibold">{{ text }}</p>
        </div>
        <CircleDashed :class="['text-sm inline-block', animate]"></CircleDashed>
    </div>
</template>

<script setup>
defineProps({
    icon: [Function, Object],
    text: String,
    color: String,
    animate: String,
})
import { CircleDashed, Dot } from 'lucide-vue-next'
</script>
