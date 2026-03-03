<template>
    <div
        class="min-h-screen bg-[#0a0a0c] flex items-center justify-center p-6 font-sans text-white selection:bg-cyan-500">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[120px] pointer-events-none">
        </div>
        <div
            class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none">
        </div>

        <div class="relative w-full max-w-2xl text-center space-y-12">
            <header class="space-y-4">
                <div class="flex justify-center">
                    <div class="p-3 bg-yellow-400/10 rounded-2xl border border-yellow-400/20 animate-pulse">
                        <Star class="w-8 h-8 text-yellow-400 fill-yellow-400" />
                    </div>
                </div>

                <h1
                    class="text-6xl md:text-7xl font-black tracking-tight bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-500 bg-clip-text text-transparent italic">
                    FITNESS ADVENTURE
                </h1>

                <div class="space-y-2">
                    <p class="text-xl font-bold text-gray-200 uppercase tracking-widest">Exercise Your Way to Victory!
                    </p>
                    <p class="text-gray-400 max-w-md mx-auto leading-relaxed">
                        Battle enemies, complete quests, and level up by doing real exercises
                    </p>
                </div>
            </header>

            <div
                class="grid grid-cols-3 gap-4 p-8 bg-white/5 border border-white/10 rounded-[2.5rem] backdrop-blur-xl shadow-2xl relative overflow-hidden group">
                <div
                    class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full duration-1000 transition-transform">
                </div>

                <div class="flex flex-col items-center space-y-3">
                    <div
                        class="w-14 h-14 rounded-full bg-cyan-500/20 flex items-center justify-center border border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                        <Crown class="w-7 h-7 text-cyan-400" />
                    </div>
                    <div>
                        <p class="text-2xl font-black">Level 1</p>
                        <p class="text-[10px] uppercase tracking-tighter text-gray-500 font-bold">Your Rank</p>
                    </div>
                </div>

                <div class="flex flex-col items-center space-y-3 border-x border-white/10">
                    <div
                        class="w-14 h-14 rounded-full bg-orange-500/20 flex items-center justify-center border border-orange-500/40 shadow-[0_0_15px_rgba(249,115,22,0.3)]">
                        <Trophy class="w-7 h-7 text-orange-400" />
                    </div>
                    <div>
                        <p class="text-2xl font-black">0</p>
                        <p class="text-[10px] uppercase tracking-tighter text-gray-500 font-bold">Gold Coins</p>
                    </div>
                </div>

                <div class="flex flex-col items-center space-y-3">
                    <div
                        class="w-14 h-14 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/40 shadow-[0_0_15px_rgba(168,85,247,0.3)]">
                        <Zap class="w-7 h-7 text-purple-400 fill-purple-400/20" />
                    </div>
                    <div>
                        <p class="text-2xl font-black">0</p>
                        <p class="text-[10px] uppercase tracking-tighter text-gray-500 font-bold">Experience</p>
                    </div>
                </div>
            </div>

            <button
                class="group relative px-12 py-5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl font-black text-xl flex items-center gap-3 mx-auto transition-all hover:scale-105 hover:shadow-[0_0_40px_rgba(6,182,212,0.5)] active:scale-95">
                <Play class="w-6 h-6 fill-white" />
                START ADVENTURE
            </button>
        </div>
    </div>
</template>

<script setup>
import { Crown, Trophy, Zap, Star, Play } from 'lucide-vue-next';
</script>
