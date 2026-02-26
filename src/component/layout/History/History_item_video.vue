<template>
    <div class="bg-gray-700/50 p-6 rounded-2xl flex items-start gap-4 max-[80%]">
        <div class="flex items-center gap-3">
            <input type="checkbox" class="w-4 h-4 rounded border-gray-600 bg-transparent"
                @click="emit('select_video', video.output_path)">
            <div class="w-32 h-20 bg-[#121212] rounded-lg flex items-center justify-center border border-gray-800">
                <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z">
                    </path>
                </svg>
            </div>
        </div>

        <div class="flex-1">
            <div class="flex justify-between items-start mb-1">
                <title_content :title="video.type" :content="video.size_video"></title_content>
                <div class="flex items-center gap-2">
                    <button
                        class="bg-gray-700/50 text-[#4fd1ed] px-4 py-1.5 rounded-lg flex items-center gap-2 text-sm font-medium">
                        <span class="animate-pulse">⚡</span> Comming
                    </button>
                    <button @click="isOpen = !isOpen"
                        class="text-gray-400 inline-block relative hover:bg-gray-700/50 p-3 hover:rounded-2xl">⋮
                        <div v-if="isOpen" class="text-xs bg-gray-700 text-white mt-8 cursor-pointer z-50 absolute top-5 right-0 w-48 overflow-y-auto ease-in-out duration-300 transition-all
                         rounded-2xl items-center">
                            <icon_title :icon="Eye" title="Show Detail" @click="switch_dashbroad(video.output_path)">
                            </icon_title>
                            <icon_title :icon="Trash2" title="Delete" color="text-red-400"
                                @click="deleteThisVideo(video.output_path)" class="border-t-2 border-gray-700">
                            </icon_title>
                        </div>
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-4 mt-2">
                <div>
                    <p class="text-gray-500 text-xs uppercase tracking-wider">Duration</p>
                    <p class="font-bold text-lg">00:00</p>
                </div>
                <div>
                    <p class="text-gray-500 text-xs uppercase tracking-wider">Reps</p>
                    <p class="font-bold text-lg">{{ video.count_good }}</p>
                </div>
                <div>
                    <p class="text-gray-500 text-xs uppercase tracking-wider">Form</p>
                    <p class="font-bold text-lg">comming</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useNavigation } from '../../../composable/helpers';
const { switch_dashbroad } = useNavigation()
import title_content from '../../bases/title_content.vue';
import { FileCheckCornerIcon, Eye, Trash2, View } from 'lucide-vue-next'
import Icon_title from '../../bases/Icon_title.vue';
import { useVideo } from '../../../store/video.store';
const videoStore = useVideo()
const deleteThisVideo = (path) => {
    const data = {
        "output_path": path,
    }
    console.log(data)
    videoStore.delete_video_store(data)
}

const isOpen = ref(false)
const emit = defineEmits(["select_video"])

defineProps({ video: Object })
</script>