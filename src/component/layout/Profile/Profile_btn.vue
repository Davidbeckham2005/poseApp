<template>
    <button
        class="bg-cyan-600/10 border border-cyan-500/50 text-cyan-400 px-4 py-2 rounded-xl hover:bg-cyan-500 hover:text-black transition-all text-sm font-semibold">
        {{ text }}
    </button>
</template>

<script setup>
defineProps({ text: String })
</script>
