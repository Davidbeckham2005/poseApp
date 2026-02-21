<template>
    <div :class="['flex flex-row justify-between text-xs', color]">
        <div>Reps {{ count }}</div>
        <div class="truncate">{{ require }}</div>
    </div>
</template>

<script setup>
defineProps({
    count: Number,
    require: String,
    color: String
})
</script>
