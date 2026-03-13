<script setup>
defineProps({
    item: Object,
    isActive: Boolean
})
const emit = defineEmits(['select'])
import { get_status_upload_video } from '../../../composable/helpers';

const isLoading = get_status_upload_video()
</script>

<template>
    <a href="#"
        :class="['flex items-center space-x-3 p-3 rounded-2xl active:scale-95 active:translate-y-0.5 mb-0.5',
            isActive ? 'dark:dark:bg-orange-400 bg-cyan-500 text-black' : 'dark:hover:bg-gray-800/50 hover:bg-cyan-500/20']"
        @click.prevent=" !isLoading && emit('select', item)">
        <component :is="item.icon" class="w-5 h-5"></component>
        <span class="font-medium uppercase">{{ item.label }}</span>
    </a>

</template>