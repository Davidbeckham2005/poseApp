<template>
    <tutorial v-if="is_tutorial" @skip_tutorial="skip_tutorial"></tutorial>
    <div v-else>
        <div class="min-h-screen relative bg-[#0a0a0a] text-white p-6">
            <Back_btn></Back_btn>

            <menu_banner></menu_banner>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl mx-auto">
                <div v-for="card in menuCards" :key="card.title"
                    :class="[card.bg, 'group relative p-8 rounded-[2rem] cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl shadow-lg min-h-[180px]']">

                    <div v-if="card.tag"
                        class="absolute top-6 right-6 px-3 py-1 rounded-full text-[10px] font-black bg-yellow-400 text-black">
                        {{ card.tag }}
                    </div>

                    <div class="h-full flex flex-col justify-between">
                        <component :is="card.icon" :size="32" class="mb-4 text-white/90" />
                        <div>
                            <h2 class="text-2xl font-extrabold mb-1">{{ card.title }}</h2>
                            <p class="text-white/80 text-sm font-medium">{{ card.desc }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-12 flex justify-center">
                <button @click="watch_tutorial"
                    class="flex items-center gap-2 text-gray-500 hover:text-white transition-colors text-sm font-bold uppercase tracking-widest">
                    <BookOpen :size="18" />
                    Hướng dẫn
                </button>
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue'
import menu_banner from './menu_banner.vue'
import Back_btn from '../../bases/Back_btn.vue'
import tutorial from '../tutorial/tutorial.vue'
const is_tutorial = ref(true)
const skip_tutorial = () => {
    is_tutorial.value = false
}
const watch_tutorial = () => {
    is_tutorial.value = true
}
import {
    Swords, Crown, Star, Trophy,
    Skull, Target, User, ChevronLeft,
    Settings, Play, BookOpen
} from 'lucide-vue-next';

// Giả lập dữ liệu user
const stats = [
    { label: 'Level', value: '5', icon: Crown, color: 'text-yellow-400' },
    { label: 'XP', value: '450', icon: Star, color: 'text-blue-400' },
    { label: 'Rank', value: 'Warrior', icon: Trophy, color: 'text-orange-400' },
];

const menuCards = [
    {
        title: 'Start Battle',
        desc: 'Fight monsters with real exercises',
        icon: Swords,
        bg: 'bg-gradient-to-br from-blue-500 to-cyan-400'
    },
    // {
    //     title: 'Boss Mode',
    //     desc: 'Face powerful boss monsters',
    //     icon: Skull,
    //     bg: 'bg-gradient-to-br from-red-500 to-gray-500',
    //     tag: 'HARD'
    // },
    // {
    //     title: 'Daily Quests',
    //     desc: 'Complete challenges for rewards',
    //     icon: Target,
    //     bg: 'bg-gradient-to-br from-purple-500 to-pink-500',
    //     tag: '0/3'
    // },
    // {
    //     title: 'Character',
    //     desc: 'View your transformation journey',
    //     icon: User,
    //     bg: 'bg-gradient-to-br from-green-500 to-emerald-400'
    // },
];
</script>