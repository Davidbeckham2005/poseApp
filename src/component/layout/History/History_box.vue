<template>
    <div class="aspect-[4/3] h-32 border-white/20 border rounded-2xl bg-gray-700/50 p-2 pl-5 items-center">
        <div class="flex justify-between pt-1 pb-1">
            <span class="text-gray-500 text-sm">{{ item.first_line }}</span>
            <component :is="item.icon" :class='["text-xs text-cyan-400", item.color_icon]'></component>
        </div>
        <p class="text-2xl font-semibold text-white">{{ item.middle_value }}</p>
        <span :class='["text-gray-500 text-sm", item.green_line]'>{{ item.last_line }}</span>
    </div>
</template>

<script setup>
defineProps({
    item: Object,
})
</script>
