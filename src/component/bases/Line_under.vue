<template>
    <p class="text-gray-500 mb-4 text-sm border-b pb-2 border-gray-700/30">{{ text }}</p>
</template>

<script setup>
defineProps({
    text: String,
    size: {
        type: String,
        default: "text-sm"
    }
})
</script>
