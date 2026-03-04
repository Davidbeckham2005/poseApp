<template>
    <pose_advanture_lobby v-if="current_layout == 'lobby'"></pose_advanture_lobby>
    <!-- <pose_advanture_menu v-else-if="current_layout == 'menu'"></pose_advanture_menu> -->
    <!-- <pose_advanture_menu></pose_advanture_menu> -->
</template>

<script setup>
// cac component
import pose_advanture_lobby from './pose_advanture_lobby.vue';
import pose_advanture_menu from './pose_advanture_menu.vue';

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
