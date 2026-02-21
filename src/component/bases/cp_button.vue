<script setup>
const props = defineProps(['icon']);
</script>

<template>
    <div>
        <button class="flex items-center px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-xl transition group">
            <component :is="icon" class="w-7 h-7 fill-current group-hover:scale-110 transition"></component>
        </button>
    </div>
</template>