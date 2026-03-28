<template>
    <div class="fixed left-40 top-4 z-50">
        <div class="flex flex-row items-center gap-4 px-4 py-2 
                bg-slate-900/80 backdrop-blur-xl border border-white/10 
                rounded-full shadow-2xl shadow-emerald-500/10 transition-all hover:border-emerald-500/30">

            <div class="relative flex items-center justify-center w-8 h-8">
                <div class="absolute inset-0 rounded-full border border-emerald-500/20"></div>
                <div @click="togglePlay" :class="['text-xl transition-all duration-[30000ms] linear infinite',
                    isPlaying ? 'animate-spin' : 'opacity-50']">
                    💿
                </div>
                <div class="absolute w-1.5 h-1.5 bg-slate-900 rounded-full border border-emerald-400"></div>
            </div>

            <div class="flex flex-col border-l border-white/10 pl-3">
                <span class="text-[9px] uppercase tracking-[0.15em] text-slate-500 font-black leading-none mb-1">
                    Audio
                </span>
                <span class="text-[11px] font-bold text-white tracking-wide truncate w-28 drop-shadow-sm">
                    {{ currentTrackName }}
                </span>
            </div>

            <button @click="nextTrack" class="group flex items-center justify-center p-1.5 rounded-full 
                   bg-white/5 hover:bg-emerald-500 text-slate-400 hover:text-white">
                <CircleArrowRight class="w-5 h-5 transition-transform duration-500 " />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { CircleArrowRight } from 'lucide-vue-next'
import { useAudio } from '../../composable/audio';
const { globalVolume, playBGM, stopBGM, currentTrack, tracks } = useAudio()
const isPlaying = ref(true)
const TrackList = tracks
const currentTrackName = computed(() => {
    return currentTrack.value
})
const nextTrack = () => {
    const currentIndex = TrackList.indexOf(currentTrack.value)
    const nextIndex = (currentIndex + 1) % TrackList.length
    playBGM(TrackList[nextIndex])
}



const togglePlay = () => {
    isPlaying.value = !isPlaying.value
    if (isPlaying.value) {
        playBGM(currentTrackName.value)
    } else {
        stopBGM()
    }
}



// const updateVolume = (e) => {
//     setVolume(parseFloat(e.target.value))
// }
// const updateVolume = (e) => {
//     setVolume(parseFloat(e.target.value))
// }
</script>

<style lang="scss" scoped></style>
