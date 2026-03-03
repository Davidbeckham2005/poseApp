<template>
    <div class="p-5 rounded-2xl border border-white/20 hover:border-white/50 ">
        <p class="text-xs font-semibold uppercase tracking-wide flex items-center gap-2">
            {{ stat.label }}
        </p>
        <p class="text-2xl font-bold mt-2" :class="stat.color">{{ stat.value }}</p>
    </div>
</template>

<script setup>
defineProps({ stat: Object })
</script>
