<template>
    <div
        class="relative w-full max-w-5xl mx-auto bg-gradient-to-b from-indigo-600 to-purple-700 rounded-3xl p-10 text-center mb-8 overflow-hidden">
        <div
            class="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]">
        </div>

        <div class="flex flex-col items-center">
            <Swords :size="48" class="mb-4 text-white/80" />
            <h1 class="text-5xl font-black mb-2 tracking-tight">FITNESS ADVENTURE</h1>
            <p class="text-indigo-100 text-lg mb-8 opacity-80">Tập luyện mạnh mẽ – thống trị đấu trường!</p>

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
</template>

<script setup>
import {
    Swords, Crown, Star, Trophy,
} from 'lucide-vue-next';
const stats = [
    { label: 'Cấp độ', value: '5', icon: Crown, color: 'text-yellow-400' },
    { label: 'XP', value: '450', icon: Star, color: 'text-blue-400' },
    { label: 'Rank', value: 'Warrior', icon: Trophy, color: 'text-orange-400' },
];
</script>