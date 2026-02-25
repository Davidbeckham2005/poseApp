<script setup>
defineProps({
    title: String,
    content: String,
    size_title: {
        type: String,
        default: 'text-xl'
    },
    size_content: {
        type: String,
        default: 'text-sm'
    }
})
</script>

<template>
    <div class="flex flex-col">
        <h2 :class='["font-semibold text-white", size_title]'>{{ title }}</h2>
        <p :class='["text-gray-500 mb-4", size_content]'>{{ content }}</p>
    </div>
</template>