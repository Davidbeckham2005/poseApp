<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { Timer, SkipForward } from "lucide-vue-next"
import { useAudio } from "../../../composable/audio"
const { unlockAudio } = useAudio()
import { Use_is_warmup } from "../../../composable/help_game"
import Trainer from "../Trainer/Trainer.vue"
import { startPose, stopPose } from "../../../services/PoseDetector"
import { usePose } from "../../../services/detect_help"

const { get_state_warmup, set_state_warmup } = Use_is_warmup()
const { speak } = useAudio()
const { isInside } = usePose()

// Warmup exercises with mapped exercise types for backend detection
const warmups = [
    { name: "Dãn vai", time: 10, speak_voice: "Dãn vai", path: "/tutorial/Shoulder Stretch", exerciseId: "warmup_shoulder_stretch" },
    { name: "Dũi chân", time: 20, speak_voice: "Dũi chân", path: "/tutorial/Single Leg Hip Rotation", exerciseId: "warmup_hip_rotation" },
    { name: "Squat nhẹ", time: 30, speak_voice: "sờ quáp nhẹ", path: "/tutorial/Squat Reach", exerciseId: "warmup_squat" },
    { name: "Jump tại chỗ", time: 20, speak_voice: "dăm tại chổ", path: "/tutorial/Jumping Jack", exerciseId: "warmup_jumping_jack" }
]

// Refs for pose detection
const videoRef = ref(null)
const canvasRef = ref(null)
const isDetecting = ref(false)
const poseStats = ref({
    total: 0,
    good: 0,
    state: "",
    estimate: "",
    require: ""
})
const inside = computed(() => isInside.value)

const step = ref(0)
const timeLeft = ref(warmups[0].time)
let timer = null
let isPoseSpeakActive = false

const current = computed(() => warmups[step.value])

const progress = computed(() => {
    return ((current.value.time - timeLeft.value) / current.value.time) * 100
})

const warning = computed(() => {
    return isDetecting.value && !inside.value
})

// Handle pose detection results
const handlePoseResult = (data) => {
    poseStats.value = {
        total: data.total || 0,
        good: data.good || 0,
        state: data.state || "",
        estimate: data.estimate || "",
        require: data.require || ""
    }
}


function nextStep() {
    isDetecting.value = false
    stopPose()
    poseStats.value = { total: 0, good: 0, state: "", estimate: "", require: "" }

    step.value++
    if (step.value < warmups.length) {
        speak(`Bắt đầu ${warmups[step.value].speak_voice}`)
        timeLeft.value = warmups[step.value].time
        // Start pose detection for next exercise
        setTimeout(() => {
            startPoseDetection()
        }, 500)
    } else {
        clearInterval(timer)
        set_state_warmup(false)
    }
}

function startPoseDetection() {
    if (!videoRef.value || !canvasRef.value) return

    isDetecting.value = true
    const exerciseId = current.value.exerciseId

    startPose(videoRef.value, canvasRef.value, exerciseId, isDetecting, (data) => {
        handlePoseResult(data)
    })
}

function skipWarmup() {
    nextStep()
}





// Warning feedback for out of frame
watch(warning, (newValue) => {
    if (newValue && !isPoseSpeakActive) {
        isPoseSpeakActive = true
        speak("Vui lòng đứng vào khung tập để tiếp tục")
        setTimeout(() => {
            isPoseSpeakActive = false
        }, 2000)
    }
})

onMounted(async () => {
    // Request camera permission first
    try {
        await navigator.mediaDevices.getUserMedia({ video: true })
    } catch (err) {
        console.error("Camera permission denied:", err)
    }

    speak(`Bắt đầu ${warmups[0].speak_voice}`)
    startPoseDetection()

    timer = setInterval(() => {
        // Only count down timer if user is inside safe zone
        if (!inside.value) {
            return
        }

        let time = timeLeft.value - 1

        if (time == 3) speak("ba")
        if (time == 2) speak("hai")
        if (time == 1) speak("một")
        timeLeft.value--
        if (timeLeft.value <= 0) {
            nextStep()
        }
    }, 1000)
})

onUnmounted(() => {
    clearInterval(timer)
    stopPose()
    isDetecting.value = false
    speechSynthesis.cancel()
})
</script>

<template>
    <div @click.once="unlockAudio" class="flex items-center justify-center bg-gray-900 text-white min-h-screen p-4">
        <div class="w-full max-w-6xl">
            <!-- MAIN LAYOUT: TRAINER + CAMERA + STATS -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

                <!-- LEFT: Trainer Model -->
                <div class="bg-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-center">
                    <Trainer :path_json="warmups[step].path" :key="step"></Trainer>
                </div>

                <!-- CENTER: Camera with Pose Detection -->
                <div class="bg-black rounded-2xl overflow-hidden border-3 border-emerald-500/50 shadow-2xl">
                    <!-- Camera Feed -->
                    <div class="relative w-full h-[400px] bg-gray-900 rounded-2xl overflow-hidden">
                        <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover scale-x-[-1]" autoplay
                            playsinline />

                        <!-- Pose Canvas Overlay -->
                        <canvas ref="canvasRef" width="640" height="480" class="absolute inset-0 w-full h-full"
                            :class="warning ? 'blur-sm brightness-50' : ''" />

                        <!-- Warning Overlay -->
                        <div v-if="warning"
                            class="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                            <div class="text-yellow-400 text-lg font-semibold animate-pulse text-center px-4">
                                ⚠ Không phát hiện người <br />
                                Hãy đứng vào khung tập
                            </div>
                        </div>
                    </div>
                </div>

                <!-- RIGHT: Exercise Info & Stats -->
                <div class="bg-gray-800 rounded-2xl p-6 shadow-xl space-y-4">
                    <!-- Exercise Name -->
                    <div class="text-center">
                        <h2 class="text-2xl font-bold text-orange-400">{{ current.name }}</h2>
                        <p class="text-gray-400 text-sm mt-1">Khởi động</p>
                    </div>

                    <!-- Timer -->
                    <div class="bg-gray-700 rounded-xl p-4 text-center">
                        <div class="flex items-center justify-center gap-2 text-orange-400 text-3xl font-bold">
                            <Timer :size="28" />
                            {{ timeLeft }}s
                        </div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="w-full h-3 bg-gray-700 rounded-full overflow-hidden border border-gray-600">
                        <div class="h-full bg-gradient-to-r from-orange-500 to-orange-400 rounded-full transition-all duration-300"
                            :style="{ width: progress + '%' }" />
                    </div>
                    <!-- Step Indicator -->
                    <div class="text-center text-sm text-gray-400 py-2">
                        Bài {{ step + 1 }} / {{ warmups.length }}
                    </div>

                    <!-- Skip Button -->
                    <button @click="skipWarmup"
                        class="w-full flex items-center justify-center gap-2 bg-gray-700 hover:bg-gray-600 active:bg-gray-500 transition rounded-xl py-3 font-medium">
                        <SkipForward :size="18" />
                        Bỏ qua
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>