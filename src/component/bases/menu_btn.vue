<template>
    <div @click="handle_menu"
        class="z-100 flex bg-gray-700/50 px-4 py-2 rounded-2xl font-medium border border-white/20 hover:bg-gray-800/50 fixed left-3 top-3">
        <ArrowLeft></ArrowLeft>Menu
    </div>
</template>

<script setup>
import { ArrowLeft } from 'lucide-vue-next'
// import { useNavigation } from '../../composable/helpers';
import { useRouter } from 'vue-router';
const router = useRouter()

// const { switch_on_sidebar } = useNavigation()
const handle_menu = () => {
    router.push({ name: 'menu' })
}
</script>
