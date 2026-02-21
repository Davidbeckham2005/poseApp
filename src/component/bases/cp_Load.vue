<template>
    <LoaderCircle :class="['animate-spin', size]" :style="{ animationDuration: speed }"></LoaderCircle>
</template>
<script setup>
import { LoaderCircle } from 'lucide-vue-next';
defineProps({
    speed: String,
    size: {
        type: String,
        default: 'w-12 h-12'
    }
})

</script>
<style lang="scss" scoped></style>