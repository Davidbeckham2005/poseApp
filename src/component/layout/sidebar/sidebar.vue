<script setup>
import sidebar_item from "./sidebar_item.vue"
defineProps({
    menuItems: Object,
    currentTab: String
})
const emit = defineEmits(['activeMenu'])

</script>


<template>
    <aside class="justify-between p-6">
        <div>
            <div class="mb-10">
                <h1 class="text-sm md:text-2xl font-bold text-cyan-400">PoseApp</h1>
                <p class="text-xs text-gray-500 uppercase tracking-widest mt-1">Exercise Analysis</p>
            </div>
            <sidebar_item class="space-y-2" v-for="item in menuItems" :item="item" :is-active="currentTab === item.name"
                @select="emit('activeMenu', item)">
            </sidebar_item>
        </div>
        <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
            <p class="text-xs text-gray-500 uppercase">Version</p>
            <p class="text-sm font-semibold text-gray-300 tracking-wider">v1.0.0</p>
        </div>
    </aside>
</template>