<script setup>
defineProps({
    title: String,
    content: Number
})
</script>

<template>
    <div class="flex justify-between">
        <h2 class="text-lg font-semibold text-white">{{ title }}</h2>
        <p class="text-gray-500 mb-4 text-sm">{{ content }}</p>
    </div>
</template>