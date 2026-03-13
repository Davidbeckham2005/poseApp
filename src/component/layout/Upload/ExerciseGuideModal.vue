<template>
    <Transition name="fade">
        <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8">
            <div class="absolute inset-0 bg-[#0a0a0c]/80 backdrop-blur-md" @click="$emit('close')"></div>

            <div
                class="relative bg-[#1a1c1e] w-full max-w-4xl max-h-[90vh] rounded-[2.5rem] shadow-2xl border border-white/10 overflow-hidden flex flex-col md:flex-row animate-scale-up">

                <button @click="$emit('close')"
                    class="absolute top-6 right-6 z-20 p-2 bg-black/20 hover:bg-red-500/20 text-white rounded-full transition-colors group">
                    <X :size="24" class="group-hover:rotate-90 transition-transform" />
                </button>

                <div class="w-full md:w-5/12 relative bg-black flex items-center justify-center">
                    <img :src="exercise.image" class="w-full h-full object-cover opacity-80" />
                    <div class="absolute inset-0 bg-gradient-to-t from-[#1a1c1e] via-transparent"></div>

                    <div class="absolute bottom-6 left-6 flex flex-col gap-2">
                        <span
                            class="px-4 py-1.5 bg-orange-500 text-white text-[10px] font-black uppercase rounded-lg w-fit">Video
                            hướng dẫn</span>
                        <h2 class="text-3xl font-black text-white italic uppercase">{{ exercise.title }}</h2>
                    </div>
                </div>

                <div
                    class="w-full md:w-7/12 p-8 md:p-12 overflow-y-auto custom-scrollbar bg-gradient-to-br from-transparent to-orange-500/5">
                    <div class="space-y-8">
                        <div class="flex gap-8">
                            <div class="space-y-1">
                                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Thời gian</p>
                                <p class="text-xl font-black text-white">{{ exercise.time }} Phút</p>
                            </div>
                            <div class="space-y-1 border-l border-white/10 pl-8">
                                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Calo tiêu thụ
                                </p>
                                <p class="text-xl font-black text-orange-400">~{{ exercise.kcal }} kcal</p>
                            </div>
                        </div>

                        <div class="space-y-6">
                            <h3 class="flex items-center gap-3 text-lg font-black text-white uppercase tracking-tight">
                                <div
                                    class="w-8 h-8 rounded-full bg-orange-500/20 flex items-center justify-center text-orange-500 italic text-sm">
                                    01</div>
                                Hướng dẫn thực hiện
                            </h3>

                            <ul class="space-y-4">
                                <li v-for="(step, index) in exercise.steps" :key="index" class="flex gap-4 group">
                                    <div
                                        class="mt-1.5 w-1.5 h-1.5 rounded-full bg-orange-500 group-hover:scale-150 transition-transform">
                                    </div>
                                    <p class="flex-1 text-slate-400 text-sm leading-relaxed">{{ step }}</p>
                                </li>
                            </ul>
                        </div>

                        <div class="p-6 bg-blue-500/10 border border-blue-500/20 rounded-2xl space-y-2">
                            <div class="flex items-center gap-2 text-blue-400">
                                <Info :size="18" />
                                <span class="text-xs font-black uppercase tracking-widest">Mẹo từ chuyên gia</span>
                            </div>
                            <p class="text-sm text-slate-300 italic">"{{ exercise.proTip }}"</p>
                        </div>

                        <button @click.prevent="upload(exercise.type)"
                            class="w-full py-5 bg-white text-black font-black rounded-2xl hover:bg-orange-500 hover:text-white transition-all shadow-xl uppercase tracking-widest flex items-center justify-center gap-3">
                            <Play :size="20" class="fill-current" />
                            Gửi video tập luyện ngay
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { X, Info, Play } from 'lucide-vue-next';
import { useUpload } from '../../../composable/upload';
const { upload } = useUpload()
defineProps({
    isOpen: Boolean,
    exercise: {
        type: Object,
    }
});

defineEmits(['close']);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.animate-scale-up {
    animation: scaleUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes scaleUp {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(20px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}
</style>