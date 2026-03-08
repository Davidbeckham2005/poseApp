<template>
    <div @click="switch_on_sidebar('game')"
        class="z-100 flex bg-gray-700/50 px-4 py-2 rounded-2xl font-medium border border-white/20 hover:bg-gray-800/50 fixed left-3 top-3 active:scale-95">
        <ArrowLeft></ArrowLeft>Thoát
        <button>

        </button>
    </div>
</template>

<script setup>
import { ArrowLeft } from 'lucide-vue-next'
import { useNavigation } from '../../composable/helpers';
const { switch_on_sidebar } = useNavigation()

</script>
