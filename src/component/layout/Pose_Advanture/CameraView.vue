<template>
    <div class="flex flex-col items-center gap-6">
        <!-- CAMERA CONTAINER -->
        <div class="relative w-[640px] h-[480px] rounded-2xl overflow-hidden bg-slat-900 shadow-2xl">
            <!-- video -->
            <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover scale-x-[-1]" autoplay
                playsinline />
            <!-- canvas -->
            <canvas ref="canvasRef" width="640" height="480" class="absolute inset-0" :class="[
                'absolute inset-0 w-full h-full object-cover  transition duration-500',
                warning ? 'blur-md brightness-50' : ''
            ]" />
            <!-- SAFE ZONE -->
            <div class="absolute inset-0 flex items-center justify-center pointer-events-none">

                <!-- WARNING -->
                <div v-if="warning" class="absolute inset-0 flex items-center justify-center
  bg-black/40 backdrop-blur-sm text-center px-6">
                    <div class="text-red-400 text-xl font-semibold animate-pulse">
                        ⚠ Không phát hiện người <br />
                        Hãy đứng vào khung tập
                    </div>
                </div>

            </div>
            <!-- overlay label -->
        </div>
        <!-- CONTROL PANEL -->
        <div class="flex gap-4">

            <button @click="startCamera" class="px-6 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-green-400
      text-white font-medium shadow-lg hover:scale-105 hover:shadow-xl transition">
                Start
            </button>

            <button @click="stopCamera" class="px-6 py-2 rounded-xl bg-gradient-to-r from-red-500 to-rose-400
      text-white font-medium shadow-lg hover:scale-105 hover:shadow-xl transition">
                Stop
            </button>
        </div>
    </div>
</template>

<script setup>
// import
import { computed, ref } from "vue"
import { startPose, stopPose } from "../../../services/PoseDetector"
import { usePose } from "../../../services/detect_help"
import { use_analysting } from "../../../services/pose_state"


// khai bao bien
const { get_analysting } = use_analysting()
const { isInside } = usePose()
const videoRef = ref(null)
const canvasRef = ref(null)
const isStarted = ref(false)

/* trạng thái người dùng trong safe zone */
const inside = computed(() => { return isInside.value })

const startCamera = () => {
    isStarted.value = true
    startPose(videoRef.value, canvasRef.value, "lungue", isStarted)
}
``
const stopCamera = () => {
    isStarted.value = false
    stopPose()
}
const warning = computed(() => {
    return isStarted.value && !inside.value
})
</script>