<template>
    <div class="fixed inset-0 flex items-center justify-center bg-black/95 backdrop-blur-xl z-50 p-4">
        <div class="w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl bg-linear-to-b from-gray-900 via-black to-black text-white shadow-[0_0_50px_rgba(0,0,0,0.5)] border-2 animate-in zoom-in duration-300 custom-scrollbar"
            :class="win ? 'border-green-500/50 shadow-green-500/20' : 'border-red-500/50 shadow-red-500/20'">

            <div class="p-8 md:p-10">
                <div class="text-center mb-10">
                    <div class="text-8xl mb-4 drop-shadow-2xl animate-bounce">{{ win ? '🏆' : '💔' }}</div>
                    <h1 class="text-6xl font-black tracking-tighter italic"
                        :class="win ? 'text-green-400 drop-shadow-[0_0_15px_rgba(74,222,128,0.5)]' : 'text-red-400 drop-shadow-[0_0_15px_rgba(248,113,113,0.5)]'">
                        {{ win ? "VICTORY!" : "DEFEAT!" }}
                    </h1>
                    <p class="text-gray-400 mt-4 text-xl font-medium">
                        {{ win ? 'The monster has been slain!' : 'The monster was too strong this time...' }}
                    </p>
                </div>

                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div
                        class="bg-gray-800/40 rounded-2xl p-5 border border-yellow-500/30 group hover:border-yellow-500/60 transition-colors">
                        <p class="text-xs text-yellow-500 font-black uppercase tracking-widest mb-1">Total Reps</p>
                        <p class="text-4xl font-black text-white">{{ summary.total_reps }}</p>
                    </div>
                    <div
                        class="bg-gray-800/40 rounded-2xl p-5 border border-green-500/30 group hover:border-green-500/60 transition-colors">
                        <p class="text-xs text-green-500 font-black uppercase tracking-widest mb-1">Perfect Form</p>
                        <p class="text-4xl font-black text-white">{{ summary.total_good_reps }}</p>
                    </div>
                </div>

                <div class="space-y-3 mb-8">
                    <div
                        class="flex justify-between items-center bg-gray-800/30 rounded-2xl px-6 py-4 border border-gray-700 hover:bg-gray-800/50 transition-all">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">🔥</span>
                            <span class="text-lg font-bold text-gray-300">Energy Expended</span>
                        </div>
                        <span class="text-2xl font-black text-red-500">{{ summary.total_calories }} <small
                                class="text-sm">kcal</small></span>
                    </div>

                    <div
                        class="flex justify-between items-center bg-gray-800/30 rounded-2xl px-6 py-4 border border-gray-700 hover:bg-gray-800/50 transition-all">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl">🎯</span>
                            <span class="text-lg font-bold text-gray-300">Form Accuracy</span>
                        </div>
                        <span class="text-2xl font-black text-orange-500">
                            {{ summary.total_reps > 0 ? Math.floor((summary.total_good_reps / summary.total_reps) *
                                100) : 0 }}%
                        </span>
                    </div>
                </div>

                <div class="bg-gray-900/60 rounded-2xl p-6 border border-gray-800 mb-8">
                    <h3 class="text-sm font-black text-gray-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                        <span class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
                        Battle Log
                    </h3>
                    <div class="space-y-3 max-h-60 overflow-y-auto pr-3 custom-scrollbar">
                        <div v-for="(item, index) in summary.history" :key="index"
                            class="group flex justify-between items-center bg-black/40 rounded-xl p-4 border border-gray-800 hover:border-blue-500/50 transition-all">
                            <div class="flex flex-col">
                                <span class="text-base font-black text-blue-400 uppercase italic">{{ item.exercise
                                }}</span>
                                <div class="flex gap-3 text-[11px] text-gray-500 font-bold uppercase mt-1">
                                    <span>⏱️ {{ item.duration }}</span>
                                    <span>✨ {{ item.accuracy }}% Accuracy</span>
                                </div>
                            </div>
                            <div class="text-right">
                                <span class="text-xl font-black text-white">{{ item.good_reps }}<span
                                        class="text-gray-600">/</span>{{ item.actual_reps }}</span>
                                <p class="text-xs font-bold text-red-500/80 mt-1">-{{ item.calories }}kcal</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    class="bg-linear-to-r from-blue-900/30 to-purple-900/30 rounded-2xl p-6 border border-blue-500/30 mb-10">
                    <h3 class="font-black text-blue-400 uppercase text-sm tracking-widest mb-4 flex items-center gap-2">
                        <span>⚡</span> RECOVERY PROTOCOL
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="flex flex-col items-center text-center group">
                            <div class="text-3xl mb-2 group-hover:scale-125 transition-transform">💧</div>
                            <p class="text-[11px] text-gray-400 leading-tight">Uống <span
                                    class="text-white font-bold">300ml</span> nước để bù điện giải.</p>
                        </div>
                        <div
                            class="flex flex-col items-center text-center group border-y md:border-y-0 md:border-x border-gray-700 py-4 md:py-0">
                            <div class="text-3xl mb-2 group-hover:scale-125 transition-transform">🍌</div>
                            <p class="text-[11px] text-gray-400 leading-tight">Nạp <span
                                    class="text-white font-bold">Carbs nhanh</span> (chuối/sữa chua).</p>
                        </div>
                        <div class="flex flex-col items-center text-center group">
                            <div class="text-3xl mb-2 group-hover:scale-125 transition-transform">💤</div>
                            <p class="text-[11px] text-gray-400 leading-tight">Nghỉ ít nhất <span
                                    class="text-white font-bold">24h</span> để hồi cơ.</p>
                        </div>
                    </div>
                </div>

                <div class="flex gap-4 sticky bottom-0 bg-transparent pt-2">
                    <button @click="handle_menu"
                        class="group flex-1 px-8 py-5 bg-white text-black rounded-2xl font-black text-xl transition-all hover:bg-green-400 hover:scale-[1.02] active:scale-95 shadow-[0_10px_20px_rgba(255,255,255,0.1)] flex items-center justify-center gap-2 uppercase tracking-tighter">
                        Claim Rewards & Exit
                        <span class="group-hover:translate-x-1 transition-transform">→</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    summary: Object,
    win: Boolean
})
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';
const router = useRouter()
const win = ref(true)
const handle_menu = () => {
    router.push({ name: 'menu' })
}
</script>

<style lang="scss" scoped></style>