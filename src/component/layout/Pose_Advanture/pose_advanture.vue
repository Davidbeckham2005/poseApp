<template>
    <lobby v-if="current_layout == 'lobby'"></lobby>
</template>
<script setup>
import lobby from './lobby.vue';
import { useNavigation } from '../../../composable/help_game';
import { computed, ref } from 'vue'

const { get_current_layout } = useNavigation()
const current_layout = computed(() => {
    return get_current_layout()
})
</script>
