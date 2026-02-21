<template>
    <div class="rounded-2xl bg-gray-700/50 p-2 h-20 w-full pl-5">
        <p class="text-gray-500 text-sm">Exercise</p>
        <p class="text-lg font-semibold text-white">{{ exercise }}</p>
    </div>
</template>

<script setup>
defineProps({
    exercise: String
})
</script>

<style lang="scss" scoped></style>
