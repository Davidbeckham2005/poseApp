<script setup>
defineProps({
    title: String,
    content: String,
    // size: String = "text-xl"
})
</script>

<template>
    <div class="flex flex-col">
        <h2 class="text-xl font-semibold text-white">{{ title }}</h2>
        <p class="text-gray-500 mb-4 text-sm">{{ content }}</p>
    </div>
</template>