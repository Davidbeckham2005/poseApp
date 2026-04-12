<template>
    <div class="flex flex-col items-center gap-6">
        <!-- CAMERA CONTAINER -->
        <div class="relative w-160 h-120 rounded-2xl overflow-hidden bg-slate-900 shadow-2xl">
            <!-- video -->
            <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover transition duration-500"
                :class="isStarted ? 'saturate-125 contrast-110' : ''" autoplay playsinline />
            <!-- canvas -->
            <canvas ref="canvasRef" width="640" height="480" class="absolute inset-0" :class="'absolute inset-0 w-full h-full object-cover  transition duration-500',
                warning ? 'blur-md brightness-50' : ''
                " />

            <!-- ACTIVE CAMERA HUD -->
            <div v-if="isStarted" class="absolute inset-0 z-10 pointer-events-none">
                <!-- <div
                    class="absolute top-3 left-3 px-3 py-1 rounded-full bg-black/70 border border-red-400/60 text-red-300 text-xs font-black tracking-widest">
                    ● LIVE AI
                </div>
                <div class="absolute top-3 right-3 px-3 py-1 rounded-full bg-black/70 text-xs font-bold"
                    :class="inside ? 'text-emerald-300 border border-emerald-400/60' : 'text-amber-300 border border-amber-400/60'">
                    {{ inside ? 'IN FRAME' : 'OUT OF FRAME' }}
                </div> -->

                <div class="absolute inset-6 rounded-xl border border-cyan-400/20"></div>
                <div class="scanline absolute inset-x-0 h-0.5 bg-cyan-300/70"></div>

                <div class="absolute bottom-3 inset-x-3 rounded-lg bg-black/65 border border-cyan-400/30 px-3 py-2">
                    <p class="text-[11px] uppercase tracking-widest text-cyan-300 font-black mb-1">Live Coach</p>
                    <p class="text-sm text-slate-100 leading-tight">{{ overlayTip }}</p>
                </div>
            </div>

            <!-- CAMERA TUTORIAL OVERLAY -->
            <div v-if="!isStarted"
                class="absolute inset-0 z-10 bg-black/70 backdrop-blur-sm flex items-center justify-center p-6">
                <div class="w-full max-w-md rounded-2xl border border-cyan-400/40 bg-slate-900/90 p-5 text-left">
                    <p class="text-xs uppercase tracking-widest text-cyan-300 font-bold mb-3">Camera Setup</p>
                    <h3 class="text-lg font-black text-white mb-3">Bật camera để bắt đầu phân tích</h3>
                    <ul class="text-sm text-slate-200 space-y-2 leading-relaxed">
                        <li>1. Nhấn Start để bật camera AI.</li>
                        <li>2. Nếu trình duyệt hỏi quyền, chọn Allow camera.</li>
                        <li>3. Đứng giữa khung và giữ đủ ánh sáng.</li>
                    </ul>
                    <p class="mt-4 text-xs text-slate-400">
                        Mẹo: Nếu vẫn đen màn hình, kiểm tra camera không bị app khác chiếm dụng.
                    </p>
                </div>
            </div>

            <!-- SAFE ZONE -->
            <div class="absolute inset-0 flex items-center justify-center pointer-events-none">

                <!-- WARNING -->
                <div v-if="warning" class="absolute inset-0 flex items-center justify-center
    bg-black/40 backdrop-blur-sm text-center px-6 z-20">
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
                Start
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
const props = defineProps({ exercise_type: String, currentHp: Number, workoutPlan: { type: Array, default: () => [] } })
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
    startPose_game2(videoRef.value, canvasRef.value, isStarted, emit, handleResult, handle_game, props.workoutPlan)
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
const overlayTip = computed(() => {
    if (warning.value) return "Di chuyển vào giữa khung để hệ thống nhận diện chính xác."
    const tips = exercise_tips.value || []
    if (tips.length === 0) return "Giữ thân người ổn định, tập đúng nhịp để đạt điểm tốt."
    return tips[tipIndex.value % tips.length]
})
onUnmounted(() => {
    stopCamera()
}) 
</script>

<style scoped>
@keyframes scanlineMove {
    0% {
        top: 12%;
        opacity: 0.2;
    }

    50% {
        opacity: 0.9;
    }

    100% {
        top: 88%;
        opacity: 0.2;
    }
}

.scanline {
    animation: scanlineMove 2.2s linear infinite;
    box-shadow: 0 0 14px rgba(103, 232, 249, 0.8);
}
</style>