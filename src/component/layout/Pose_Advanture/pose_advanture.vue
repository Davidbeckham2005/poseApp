<template>
    <lobby v-if="current_layout == 'lobby'"></lobby>
</template>

<script setup>
// cac component
import lobby from './lobby.vue';
import { useNavigation } from '../../../composable/help_game';


import { computed, ref } from 'vue'
const layout = computed(() => [
    'lobby', 'menu'
])
const { get_current_layout } = useNavigation()
const current_layout = computed(() => {
    return get_current_layout()
})
</script>
<!-- <template>
    <div>

    </div>
</template>

<script setup>

</script>

<style lang="scss" scoped></style> -->