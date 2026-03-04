<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex flex-col">

        <!-- Header -->
        <header class="flex justify-between items-center p-6">
            <h1 class="text-3xl font-bold tracking-wide">
                Choose Your Training Mode
            </h1>

            <div class="flex items-center gap-3">
                <div class="text-right">
                    <p class="text-sm text-gray-400">Level</p>
                    <p class="font-bold text-lg text-green-400">12</p>
                </div>
                <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center font-bold">
                    HK
                </div>
            </div>
        </header>

        <!-- Game Mode Grid -->
        <main class="flex-1 px-6 pb-10">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

                <div v-for="mode in modes" :key="mode.name" @click="selectMode(mode)"
                    class="relative bg-slate-800 rounded-2xl p-6 shadow-lg cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:border hover:border-green-400"
                    :class="mode.locked ? 'opacity-50 cursor-not-allowed hover:scale-100 hover:border-none' : ''">
                    <!-- Lock Overlay -->
                    <div v-if="mode.locked"
                        class="absolute inset-0 bg-black/60 rounded-2xl flex items-center justify-center text-xl font-bold">
                        🔒 Locked
                    </div>

                    <div class="text-4xl mb-4">
                        {{ mode.icon }}
                    </div>

                    <h2 class="text-xl font-semibold mb-2">
                        {{ mode.name }}
                    </h2>

                    <p class="text-gray-400 text-sm mb-4">
                        {{ mode.description }}
                    </p>

                    <div class="flex justify-between items-center">
                        <span class="px-3 py-1 text-xs rounded-full" :class="difficultyColor(mode.difficulty)">
                            {{ mode.difficulty }}
                        </span>

                        <button v-if="!mode.locked"
                            class="bg-green-500 hover:bg-green-400 px-4 py-2 rounded-lg text-sm font-semibold transition">
                            Start
                        </button>
                    </div>
                </div>

            </div>
        </main>

        <!-- Daily Quest -->
        <footer class="bg-slate-800 p-6 border-t border-slate-700">
            <h3 class="text-lg font-semibold mb-3">🔥 Daily Quest</h3>
            <ul class="space-y-2 text-gray-300 text-sm">
                <li>• Do 30 Squats</li>
                <li>• Hold Plank 60 seconds</li>
                <li>• Complete 20 Push-ups</li>
            </ul>
        </footer>

    </div>
</template>

<script setup>
import { state_game } from '../../../composable/help_game'
const { set_state_game } = state_game()
import { onMounted, ref } from 'vue'



const modes = ref([
    {
        name: 'Push-up Battle',
        icon: '💪',
        description: 'Build upper body strength and attack monsters.',
        difficulty: 'Easy',
        locked: false
    },
    {
        name: 'Squat Smash',
        icon: '🦵',
        description: 'Crush enemies with powerful leg strikes.',
        difficulty: 'Medium',
        locked: false
    },
    {
        name: 'Plank Defense',
        icon: '🛡️',
        description: 'Hold position to block boss attacks.',
        difficulty: 'Hard',
        locked: false
    },
    {
        name: 'Jumping Jack Storm',
        icon: '⚡',
        description: 'Fast cardio combo damage.',
        difficulty: 'Hard',
        locked: true
    }
])

const selectMode = (mode) => {
    if (mode.locked) return
    console.log('Selected mode:', mode.name)
    // sau này mày router.push sang màn game
}

const difficultyColor = (level) => {
    switch (level) {
        case 'Easy':
            return 'bg-green-500/20 text-green-400'
        case 'Medium':
            return 'bg-yellow-500/20 text-yellow-400'
        case 'Hard':
            return 'bg-red-500/20 text-red-400'
        default:
            return 'bg-gray-500/20 text-gray-400'
    }
}
</script>