<template>
    <div
        class="bg-[#1a1c1e] dark:bg-[#1a1c1e] rounded-[2rem] overflow-hidden shadow-2xl shadow-black/10 border border-black/10 transition-transform duration-300 hover:-translate-y-1">

        <div class="relative aspect-[4/3] overflow-hidden">
            <img :src="image" :alt="title" class="w-full h-full object-cover" />

            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-black/10 to-black/30"></div>

            <div :class="[
                'absolute top-4 left-4 px-4 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider',
                difficulty === 'Beginner' ? 'bg-[#3bca7d]/10 text-[#3bca7d]' : '',
                difficulty === 'Intermediate' ? 'bg-[#facc15]/10 text-[#facc15]' : '',
                difficulty === 'Advanced' ? 'bg-[#f43f5e]/10 text-[#f43f5e]' : ''
            ]">
                {{ difficulty }}
            </div>

            <!-- <div -->
            <!-- class="absolute bottom-4 right-4 px-3 py-1.5 bg-[#0a0a0c]/80 backdrop-blur-sm rounded-xl flex items-center gap-1.5 border border-white/5 shadow-inner"> -->
            <!-- <Star class="w-4 h-4 text-yellow-400 fill-yellow-400" /> -->
            <!-- <span class="text-white font-black text-xs">{{ rating }}%</span> -->
            <!-- </div> -->
        </div>

        <div class="p-6 space-y-5">
            <div class="space-y-2">
                <h3 class="text-2xl font-extrabold dark:text-white text-gray-100 tracking-tight">{{ title }}</h3>
                <p class="text-gray-400 text-sm leading-relaxed line-clamp-2">{{ description }}</p>
            </div>

            <div class="flex items-center gap-6 border-y border-black/10 py-4">
                <div class="flex items-center gap-2 text-slate-400 text-sm font-medium">
                    <Clock :size="16" class="text-cyan-400" /> {{ time }} min
                </div>
                <div class="flex items-center gap-2 text-slate-400 text-sm font-medium">
                    <Zap :size="16" class="text-amber-400" /> {{ kcal }} kcal
                </div>
            </div>

            <!-- <div class="flex items-center gap-2.5 pt-1">
                <span v-for="muscle in muscles" :key="muscle"
                    class="px-4 py-2 bg-[#25282b] rounded-full text-xs font-bold text-slate-300 border border-white/5 uppercase">
                    {{ muscle }}
                </span>
                <span
                    class="px-3.5 py-2 bg-[#25282b] rounded-full text-xs font-bold text-slate-500 border border-white/5">
                    +1
                </span>
            </div> -->

            <div class="pt-2">
                <button @click.stop="upload(type)"
                    class="w-full flex items-center justify-center gap-3 dark:bg-[#248da5]/10 hover:bg-[#248da5]/20 text-[#248da5] py-4 rounded-xl font-bold transition-colors shadow-inner border border-[#248da5]/15">
                    <span class="text-sm">Tải video lên</span>
                    <ChevronRight :size="16" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Star, Clock, Zap, ChevronRight } from 'lucide-vue-next';

// Định nghĩa các props để component có thể tái sử dụng
defineProps({
    image: { type: String, required: true },
    difficulty: { type: String, default: 'Beginner' }, // e.g., 'Beginner', 'Intermediate'
    rating: { type: Number, required: true },
    title: { type: String, required: true },
    description: { type: String, required: true },
    time: { type: String, required: true }, // e.g., '10-15'
    kcal: { type: Number, required: true },
    muscles: { type: Array, default: () => [] }, // e.g., ['Quadriceps', 'Glutes']
    type: { type: String, default: "" }
});
import { useUpload } from '../../../composable/upload';
const { upload } = useUpload()
</script>