<template>
    <div>
        <div class="rounded-2xl bg-gray-700/50 p-2 sm:h-40 sm:w-32 w-40 pl-5 items-center">
            <component :is="icon" :class="['w-12 h-12 rounded-lg bg-zinc-700 p-2 mt-4', text_color]"></component>
            <p class="text-gray-500 text-sm">{{ type }}</p>
            <p class="text-2xl font-semibold text-white">{{ value }}</p>
        </div>
    </div>
</template>
<script setup>
defineProps({
    type: String,
    value: Number,
    icon: [Object, Function],
    text_color: String
})
</script>

<style lang="scss" scoped></style>