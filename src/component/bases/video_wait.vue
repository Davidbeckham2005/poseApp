<template>
    <div class="max-w-6xl border-2 border-dashed border-gray-700 rounded-2xl
        bg-stone-900/70 p-10 sm:p-20 flex flex-col items-center justify-center text-center cursor-pointer
        hover:border-cyan-400/60 transition group">
        <div
            class="hidden md:w-30 md:h-30 bg-gray-800 rounded-full sm:flex items-center justify-center mb-6 group-hover:scale-110 transition">
            <component :is="main_icon" class="text-cyan-400 w-8 h-8" />
        </div>
        <title_content :title="title" :content="content"></title_content>
        <div class="flex items-center sm:space-x-4 text-xs text-gray-600">
            <component :is="small_icon" class="w-4 h-4 mr-1" />{{ small_text }}
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    content: String,
    main_icon: Object,
    small_icon: Object,
    small_text: String,
})
import title_content from './title_content.vue';
</script>
