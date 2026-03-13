<template>
    <div class="grid grid-cols-1 gap-2 lg:grid-cols-4">
        <History class="border border-white/20 col-span-3"></History>
        <div class="rounded-2xl dark:bg-gray-700/50 p-3 mt-5 space-y-5 border border-black/20">
            <show_profile_value v-for="stat in stats" :stat="stat"></show_profile_value>
        </div>
    </div>
</template>

<script setup>
import History from '../History/History.vue';
import show_profile_value from './show_profile_value.vue';
defineProps({
    stats: Array
})
</script>
