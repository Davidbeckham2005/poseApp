<template>
    <div class="rounded-2xl bg-gray-700/50 p-3 mt-5 space-y-5">
        <Title_content_horizontal title="Recents video" :content="videoStore.total_video"
            class="border-b-2 border-gray-700/30">
        </Title_content_horizontal>
        <History_item :accuracy_good="video.accuracy_good" :count="video.total" :size_video="video.size_video"
            :output_path="video.output_path" v-for="video in videoStore.videos"></History_item>
    </div>
</template>

<script setup>
import Title_content_horizontal from '../../bases/Title_content_horizontal.vue';
import History_item from './History_item.vue';
import { useVideo } from '../../../store/video.store';
import { onMounted } from 'vue';
const videoStore = useVideo()
onMounted(async () => {
    await videoStore.fetchVideo()
})
</script>
