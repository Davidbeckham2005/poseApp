<template>
    <div @click="start_game"
        class="relative min-h-screen flex items-center justify-center p-6 font-sans overflow-hidden transition-colors duration-500
               bg-slate-50 dark:bg-[#0a0a0c] text-slate-900 dark:text-white selection:bg-orange-500 selection:text-white">

        <div
            class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-400/20 dark:bg-blue-600/20 rounded-full blur-[100px] pointer-events-none">
        </div>
        <div
            class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-400/20 dark:bg-purple-600/20 rounded-full blur-[100px] pointer-events-none">
        </div>

        <div class="relative w-full max-w-2xl text-center space-y-12 z-10">
            <header class="space-y-6">
                <div class="flex justify-center">
                    <div
                        class="p-4 bg-yellow-400/10 dark:bg-yellow-400/20 rounded-3xl border border-yellow-400/30 animate-bounce shadow-[0_0_20px_rgba(250,204,21,0.3)]">
                        <Star class="w-10 h-10 text-yellow-500 fill-yellow-400" />
                    </div>
                </div>

                <div class="space-y-2">
                    <h1 class="text-6xl md:text-8xl font-black tracking-tighter italic 
                               bg-gradient-to-br from-orange-500 via-purple-500 to-pink-500 bg-clip-text text-transparent
                               drop-shadow-sm dark:drop-shadow-[0_5px_15px_rgba(249,115,22,0.4)]">
                        FITNESS<br>ADVENTURE
                    </h1>
                </div>

                <div class="space-y-4">
                    <p
                        class="text-xl md:text-2xl font-black uppercase tracking-[0.2em] text-slate-800 dark:text-slate-100">
                        Sẵn sàng để bứt phá?
                    </p>
                    <p class="text-slate-500 dark:text-slate-400 max-w-md mx-auto leading-relaxed font-medium">
                        Biến mỗi động tác hít đất, squat thành sát thương tiêu diệt quái vật. Tập luyện chưa bao giờ thú
                        vị đến thế!
                    </p>
                </div>
            </header>

            <div
                class="grid grid-cols-3 gap-4 p-1 bg-slate-200/50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-[2.5rem] backdrop-blur-xl">
                <div v-for="(stat, i) in stats" :key="i"
                    class="flex flex-col items-center py-6 px-2 rounded-[2rem] hover:bg-white dark:hover:bg-white/5 transition-colors group">
                    <div
                        :class="['w-12 h-12 rounded-2xl flex items-center justify-center mb-3 transition-transform group-hover:scale-110 shadow-lg', stat.bg]">
                        <component :is="stat.icon" :class="['w-6 h-6', stat.color]" />
                    </div>
                    <p class="text-xl font-black text-slate-800 dark:text-white">{{ stat.value }}</p>
                    <p class="text-[10px] uppercase font-bold text-slate-400 dark:text-gray-500">{{ stat.label }}</p>
                </div>
            </div>

            <div class="pt-4">
                <button
                    class="group relative px-10 py-5 bg-slate-950 dark:bg-white rounded-2xl font-black text-xl flex items-center gap-3 mx-auto 
                           text-white dark:text-slate-950 transition-all hover:scale-105 active:scale-95 shadow-2xl
                           hover:shadow-[0_20px_40px_rgba(0,0,0,0.1)] dark:hover:shadow-[0_0_40px_rgba(255,255,255,0.2)]">
                    <Play class="w-6 h-6 fill-current" />
                    BẮT ĐẦU NGAY

                    <div
                        class="absolute inset-0 rounded-2xl border-2 border-orange-500 opacity-0 group-hover:opacity-100 transition-opacity animate-pulse">
                    </div>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Crown, Trophy, Zap, Star, Play } from 'lucide-vue-next';
import { state_game, useNavigation } from '../../../composable/help_game';
import { useRouter } from 'vue-router';

const stats = [
    { label: 'Rank', value: 'Level 1', icon: Crown, bg: 'bg-orange-100 dark:bg-orange-500/20', color: 'text-orange-600 dark:text-orange-400' },
    { label: 'Thành tích', value: '0', icon: Trophy, bg: 'bg-yellow-100 dark:bg-yellow-500/20', color: 'text-yellow-600 dark:text-yellow-400' },
    { label: 'Kinh nghiệm', value: '0', icon: Zap, bg: 'bg-purple-100 dark:bg-purple-500/20', color: 'text-purple-600 dark:text-purple-400' },
]

// ... logic giữ nguyên ...
const router = useRouter()
const { set_state_game } = state_game()

const start_game = async () => {
    set_state_game(true)
    router.push({ name: 'menu' })
    set_state_game(false)
}
</script>

<style scoped>
/* Gradient Text mượt mà hơn */
h1 {
    line-height: 0.9;
}

/* Hiệu ứng trôi nổi cho các hình cầu */
.blur-[100px] {
    animation: float 10s infinite alternate ease-in-out;
}

@keyframes float {
    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(20px, 40px);
    }
}
</style>