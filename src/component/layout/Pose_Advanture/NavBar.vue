<template>
    <div class="fixed top-20 right-4 z-40 flex gap-2 flex-col">
        <!-- Voice Toggle -->
        <div class="bg-gradient-to-r from-gray-800 to-gray-900 rounded-lg border border-gray-700 p-3 backdrop-blur-md hover:border-blue-500 transition-all shadow-lg"
            :class="isAudioEnabled() ? 'border-blue-500' : 'border-red-500'">
            <button @click="toggleVoice" class="flex items-center gap-2 text-white font-semibold min-w-40">
                <span class="text-xl">
                    {{ isAudioEnabled() ? '🔊' : '🔇' }}
                </span>
                <span class="text-sm">Voice: {{ isAudioEnabled() ? 'ON' : 'OFF' }}</span>
            </button>
        </div>

        <!-- Skeleton/Pose Overlay Toggle -->
        <div class="bg-gradient-to-r from-gray-800 to-gray-900 rounded-lg border border-gray-700 p-3 backdrop-blur-md hover:border-green-500 transition-all shadow-lg"
            :class="get_skeleton() ? 'border-green-500' : 'border-red-500'">
            <button @click="toggleSkeleton" class="flex items-center gap-2 text-white font-semibold min-w-40">
                <span class="text-xl">
                    {{ get_skeleton() ? '💀' : '👤' }}
                </span>
                <span class="text-sm">Skeleton: {{ get_skeleton() ? 'ON' : 'OFF' }}</span>
            </button>
        </div>
    </div>
</template>

<script setup>

import { useAudio } from '../../../composable/audio'
const { toggleAudio, isAudioEnabled } = useAudio()
import { useSkeleton } from '../../../services/pose_state'
const { get_skeleton, set_skeleton } = useSkeleton()




const toggleVoice = () => {
    toggleAudio()
    console.log('Audio Enabled:', isAudioEnabled())
}

const toggleSkeleton = () => {
    set_skeleton(!get_skeleton())
}

</script>

<style scoped>
button {
    cursor: pointer;
    transition: all 0.3s ease;
}

button:hover {
    transform: translateX(5px);
}

button:active {
    transform: translateX(3px);
}
</style>
