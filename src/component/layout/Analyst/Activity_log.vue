<template>
    <div class="flex flex-row justify-between text-xs">
        <span class=" font-normal text-gray-500">{{ formatTime(time) }}</span>
        <div :class="color">Reps {{ count }}</div>
        <div class="truncate " :class="color">{{ require }}</div>
    </div>
</template>

<script setup>
defineProps({
    count: String,
    require: String,
    color: String,
    time: String,
})
const formatTime = (seconds) => {
    const s = Math.floor(seconds);
    const mins = Math.floor(s / 60).toString().padStart(2, '0');
    const secs = (s % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
};
</script>
