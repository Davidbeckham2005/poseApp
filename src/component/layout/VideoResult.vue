<script setup>
import title_content from '../bases/title_content.vue';

const props = defineProps({
    title: String,
    content: String,
    path_video: String,
    size_video: {
        type: String,
        default: "",
    },
    isControls: {
        type: Boolean,
        default: true,
    },
    isloop: {
        type: Boolean,
        default: false
    },
    text_video: String,
})
</script>
<template>
    <div :class="[size_video]">
        <title_content :title=title :content=content></title_content>
        <div class="rounded-3xl overflow-hidden bg-black border border-slate-800 shadow-2xl">
            <video :src=path_video class="w-full h-full aspect-video object-contain" :controls="isControls" playsinline
                :loop="isloop" autoplay>
                <!-- <source :src=path_video type="video/mp4"> -->
            </video>
        </div>
        <div class="mt-4 flex justify-between items-center text-slate-400 px-2">
            <p class="text-sm italic">{{ text_video }}</p>
            <span class="btn btn-error text-xs uppercase tracking-widest text-black font-bold">Live</span>
        </div>
    </div>
</template>