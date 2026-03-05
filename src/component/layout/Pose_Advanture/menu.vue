<template>
    <tutorial v-if="is_tutorial" @skip_tutorial="skip_tutorial"></tutorial>
    <div v-else>
        <div class="min-h-screen relative bg-[#0a0a0a] text-white p-6">
            <Back_btn></Back_btn>

            <div
                class="relative w-full max-w-5xl mx-auto bg-gradient-to-b from-indigo-600 to-purple-700 rounded-[2.5rem] p-10 text-center mb-8 overflow-hidden shadow-2xl">
                <div
                    class="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]">
                </div>

                <div class="relative z-10 flex flex-col items-center">
                    <Swords :size="48" class="mb-4 text-white/80" />
                    <h1 class="text-5xl font-black mb-2 tracking-tight">Fitness Battle Arena</h1>
                    <p class="text-indigo-100 text-lg mb-8 opacity-80">Transform Your Body. Defeat Monsters.</p>

                    <div class="flex gap-4 w-full max-w-xl">
                        <div v-for="stat in stats" :key="stat.label"
                            class="flex-1 bg-white/10 backdrop-blur-md border border-white/10 p-4 rounded-3xl flex flex-col items-center shadow-lg">
                            <div class="flex items-center gap-2 mb-1">
                                <component :is="stat.icon" :size="16" :class="stat.color" />
                                <span class="text-xs uppercase font-bold tracking-widest text-white/60">{{
                                    stat.label }}</span>
                            </div>
                            <span class="text-2xl font-black">{{ stat.value }}</span>
                        </div>
                    </div>
                </div>
            </div>

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
    {
        title: 'Boss Mode',
        desc: 'Face powerful boss monsters',
        icon: Skull,
        bg: 'bg-gradient-to-br from-red-500 to-gray-500',
        tag: 'HARD'
    },
    {
        title: 'Daily Quests',
        desc: 'Complete challenges for rewards',
        icon: Target,
        bg: 'bg-gradient-to-br from-purple-500 to-pink-500',
        tag: '0/3'
    },
    {
        title: 'Character',
        desc: 'View your transformation journey',
        icon: User,
        bg: 'bg-gradient-to-br from-green-500 to-emerald-400'
    },
];
</script>