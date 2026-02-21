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
    <a href="#" :class="['flex items-center space-x-3 p-3 rounded-2xl transition',
        isActive ? 'bg-cyan-400 text-black' : 'hover:bg-gray-800/50']"
        @click.prevent=" !isLoading && emit('select', item)">
        <component :is="item.icon" class="w-5 h-5"></component>
        <span class="font-medium">{{ item.label }}</span>
    </a>

</template>