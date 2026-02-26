<template>
    <div :class='["flex text-sm hover:bg-gray-500 hover:rounded-xl space-x-3 p-2", color]'>
        <component :is="icon" class="ml-3"></component>
        <span>{{ title }}</span>
    </div>
</template>

<script setup>

defineProps({
    color: String,
    icon: Object,
    title: String
})
</script>
