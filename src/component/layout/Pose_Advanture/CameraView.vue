<template>
    <div class="flex flex-col items-center gap-6">
        <!-- CAMERA CONTAINER -->
        <div class="relative w-160 h-120 rounded-2xl overflow-hidden bg-slat-900 shadow-2xl">
            <!-- video -->
            <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover" autoplay playsinline />
            <!-- canvas -->
            <canvas ref="canvasRef" width="640" height="480" class="absolute inset-0" :class="'absolute inset-0 w-full h-full object-cover  transition duration-500',
                warning ? 'blur-md brightness-50' : ''
                " />
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

            <button @click="startCamera" v-if="current_game === 'game1'" class="px-6 py-2 rounded-xl bg-linear-to-r from-emerald-500 to-green-400
      text-white font-medium shadow-lg hover:scale-105 hover:shadow-xl transition">
                Start
            </button>
            <button @click="start2" v-if="current_game === 'game2'" class="px-6 py-2 rounded-xl bg-linear-to-r from-emerald-500 to-green-400
      text-white font-medium shadow-lg hover:scale-105 hover:shadow-xl transition">
                Start2
            </button>

            <button @click="stopCamera" class="px-6 py-2 rounded-xl bg-linear-to-r from-red-500 to-rose-400
      text-white font-medium shadow-lg hover:scale-105 hover:shadow-xl transition">
                Stop
            </button>
        </div>
    </div>
</template>

<script setup>
// props 
const props = defineProps({ exercise_type: String, currentHp: Number })
const emit = defineEmits(['result', 'finish', 'is_analyst_active'])

// import
import { useGameChoose } from "../../../composable/help_game"
import { computed, onUnmounted, ref, watch } from "vue"
import { startPose, stopPose, startPose_game2 } from "../../../services/PoseDetector"
import { usePose } from "../../../services/detect_help"
import { useExercise } from "../../../constants/exercise"
const { get_exercise } = useExercise()
import { useAudio, playSound } from '../../../composable/audio'
// khai bao bien
const { isInside } = usePose()
const videoRef = ref(null)
const canvasRef = ref(null)
const isStarted = ref(false)
const current_exercise_type = ref(null)
const { get_game_choose, set_game_choose } = useGameChoose()
const current_game = computed(() => get_game_choose())
/* trạng thái người dùng trong safe zone */
const inside = computed(() => { return isInside.value })

const mainLoopInterval = ref(null)
const lastSpeakTime = ref(0)
const tipIndex = ref(0)
const { speak, stopSpeak } = useAudio()
const pendingSignal = ref(false)
const signal_type = ref(null)
const handleResult = (type) => {
    pendingSignal.value = true
    signal_type.value = type
}
const handle_game = () => {
    isStarted.value = false
}
const manageVoiceLogic = () => {
    if (!isStarted.value) {
        stopSpeak()
        return
    }
    const now = Date.now()
    if (pendingSignal.value) {
        pendingSignal.value = false
        playSound(signal_type.value)
        return
    }
    if (warning.value) {
        if (now - lastSpeakTime.value > 3000) {
            speak("Vui lòng đứng vào khung tập để tiếp tục bài tập")
            lastSpeakTime.value = now
        }
        return
    }
    // ưu tiên nói cảnh báo hơn tips
    const tips = exercise_tips.value || []
    if (tips.length > 0 && now - lastSpeakTime.value > 8000) {
        speak(tips[tipIndex.value])
        tipIndex.value = (tipIndex.value + 1) % tips.length
        lastSpeakTime.value = now
    }
}
watch(isStarted, (started) => {
    if (started) {
        tipIndex.value = 0
        lastSpeakTime.value = 0
        mainLoopInterval.value = setInterval(manageVoiceLogic, 500)

    } else {
        if (mainLoopInterval.value) clearInterval(mainLoopInterval.value)
        stopSpeak()
    }
})
// trạng thái của bài tập được chọn
watch(() => props.exercise_type, (newValue) => {
    current_exercise_type.value = newValue
})

// theo dõi hp của quái
watch(() => props.currentHp, (newValue) => {
    if (newValue <= 0) {
        stopCamera()
        emit('finish')
    }
})

// start camera và bắt đầu bài tập
const start2 = () => {
    isStarted.value = true
    startPose_game2(videoRef.value, canvasRef.value, isStarted, emit, handleResult, handle_game)
    emit('is_analyst_active', true)
}
const startCamera = () => {
    if (!current_exercise_type.value) {
        alert("Please choose a skill before starting the analysis.")
        return
    }
    isStarted.value = true
    startPose(videoRef.value, canvasRef.value, current_exercise_type.value, isStarted, emit)
    emit('is_analyst_active', true)
}

//  stop camera và dừng bài tập
const stopCamera = () => {
    isStarted.value = false
    if (mainLoopInterval.value) clearInterval(mainLoopInterval.value)
    stopPose()
    emit('is_analyst_active', false)
}

// cảnh báo khi người dùng không đứng trong safe zone
const warning = computed(() => {
    return isStarted.value && !inside.value
})
const exercise_tips = computed(() => { return get_exercise(props.exercise_type)?.tips || [] })
onUnmounted(() => {
    stopCamera()
}) 
</script>