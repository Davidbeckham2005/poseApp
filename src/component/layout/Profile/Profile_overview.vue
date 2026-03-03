<template>
    <div class="mx-auto grid grid-cols-1 gap-2 lg:grid-cols-4 space-x-1.5 p-5">
        <History class="border border-white/20 col-span-3"></History>
        <div class="rounded-2xl bg-gray-700/50 p-3 mt-5 space-y-5 border border-white/20">
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
