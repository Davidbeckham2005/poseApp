<template>
    <button
        class="dark:bg-orange-600/10 border border-orange-500/50 text-orange-400 px-4 py-2 rounded-xl hover:dark:bg-orange-500 hover:text-black transition-all text-sm font-semibold">
        {{ text }}
    </button>
</template>

<script setup>
defineProps({ text: String })
</script>
