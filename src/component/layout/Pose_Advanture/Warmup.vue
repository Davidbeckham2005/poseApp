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

const warmups = [
    { name: "Dãn vai", time: 10, speak_voice: "Dãn vai", path: "/tutorial/Shoulder Stretch", exerciseId: "warmup_shoulder_stretch" },
    { name: "Dũi chân", time: 20, speak_voice: "Dũi chân", path: "/tutorial/Single Leg Hip Rotation", exerciseId: "warmup_hip_rotation" },
    { name: "Squat nhẹ", time: 30, speak_voice: "sờ quáp nhẹ", path: "/tutorial/Squat Reach", exerciseId: "warmup_squat" },
    { name: "Jump tại chỗ", time: 20, speak_voice: "dăm tại chổ", path: "/tutorial/Jumping Jack", exerciseId: "warmup_jumping_jack" }
]

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
let warningResetTimer = null
let lastWarningSpeakAt = 0
const warningCooldownMs = 3000

const current = computed(() => warmups[step.value])

const progress = computed(() => {
    return ((current.value.time - timeLeft.value) / current.value.time) * 100
})

const warning = computed(() => {
    return isDetecting.value && !inside.value
})

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

const handleWarningChange = (newValue) => {
    if (!newValue) return

    const now = Date.now()
    if (isPoseSpeakActive || now - lastWarningSpeakAt < warningCooldownMs) return

    lastWarningSpeakAt = now
    isPoseSpeakActive = true
    speak("Vui lòng đứng vào khung tập để tiếp tục")

    if (warningResetTimer) clearTimeout(warningResetTimer)
    warningResetTimer = setTimeout(() => {
        isPoseSpeakActive = false
        warningResetTimer = null
    }, 2000)
}

watch(warning, handleWarningChange)

onMounted(async () => {
    try {
        await navigator.mediaDevices.getUserMedia({ video: true })
    } catch (err) {
        console.error("Camera permission denied:", err)
    }

    speak(`Bắt đầu ${warmups[0].speak_voice}`)
    startPoseDetection()

    timer = setInterval(() => {
        if (!inside.value) {
            return
        }

        timeLeft.value--
        const time = timeLeft.value

        if (time == 3) speak("ba")
        if (time == 2) speak("hai")
        if (time == 1) speak("một")

        if (timeLeft.value <= 0) {
            nextStep()
        }
    }, 1000)
})

onUnmounted(() => {
    clearInterval(timer)
    if (warningResetTimer) clearTimeout(warningResetTimer)
    stopPose()
    isDetecting.value = false
    speechSynthesis.cancel()
})
</script>

<template>
    <div @click.once="unlockAudio" class="min-h-screen overflow-hidden bg-[#050816] text-white relative">
        <!-- Animated Background Blobs -->
        <div class="absolute inset-0 pointer-events-none">
            <div class="absolute -top-32 -left-32 h-80 w-80 rounded-full bg-cyan-500/20 blur-3xl"></div>
            <div class="absolute top-1/3 -right-24 h-96 w-96 rounded-full bg-orange-500/20 blur-3xl"></div>
            <div class="absolute bottom-0 left-1/4 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl"></div>
        </div>

        <div class="relative mx-auto max-w-7xl px-4 py-6 lg:px-8 lg:py-8">
            <!-- Header -->
            <div class="mb-8 text-center">
                <p class="text-xs uppercase tracking-[0.35em] text-orange-300/80">Chuẩn bị sức</p>
                <h1 class="text-4xl font-black tracking-tight sm:text-5xl">Khởi động</h1>
                <p class="mt-2 text-white/60">Bài {{ step + 1 }} / {{ warmups.length }}</p>
            </div>

            <!-- Main Layout: 3 Columns -->
            <div class="grid gap-6 lg:grid-cols-[1fr_1.3fr_1fr]">

                <!-- LEFT: Trainer Model -->
                <section class="rounded-4xl border border-white/10 bg-white/5 p-5 shadow-2xl backdrop-blur-xl">
                    <div class="flex flex-col h-full">
                        <p class="text-xs font-bold uppercase tracking-[0.3em] text-cyan-300/80 mb-4">Hình mẫu</p>
                        <div class="flex-1 flex items-center justify-center min-h-96">
                            <Trainer :path_json="warmups[step].path" :key="step"></Trainer>
                        </div>
                    </div>
                </section>

                <!-- CENTER: Camera with Pose Detection -->
                <section class="rounded-4xl overflow-hidden border border-emerald-500/30 shadow-2xl min-h-96">
                    <div class="relative w-full h-full bg-linear-to-br from-gray-900 to-black">
                        <!-- Camera Feed -->
                        <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover" autoplay
                            playsinline />

                        <!-- Pose Canvas Overlay -->
                        <canvas ref="canvasRef" width="640" height="480" class="absolute inset-0 w-full h-full"
                            :class="warning ? 'blur-sm brightness-50' : ''" />

                        <!-- Warning Overlay -->
                        <div v-if="warning"
                            class="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm">
                            <div class="text-center">
                                <div class="text-5xl mb-3">⚠️</div>
                                <p class="text-yellow-300 text-lg font-bold">Không phát hiện người</p>
                                <p class="text-yellow-300/70 text-sm mt-1">Hãy đứng vào khung tập</p>
                            </div>
                        </div>

                        <!-- Corner Info Badge -->

                    </div>
                </section>

                <!-- RIGHT: Exercise Info & Controls -->
                <section
                    class="rounded-4xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-xl flex flex-col">
                    <!-- Exercise Name -->
                    <div class="mb-6">
                        <p class="text-xs font-bold uppercase tracking-[0.3em] text-orange-300/80">Bài tập hiện tại</p>
                        <h2 class="mt-2 text-3xl font-black text-orange-300">{{ current.name }}</h2>
                    </div>

                    <!-- Timer Card -->
                    <div class="mb-6 rounded-3xl border border-white/10 bg-black/20 p-6 text-center">
                        <div class="flex items-center justify-center gap-3 text-5xl font-black text-cyan-400">
                            <Timer :size="40" />
                            <span>{{ String(timeLeft).padStart(2, '0') }}s</span>
                        </div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="mb-6">
                        <div
                            class="h-3 w-full rounded-full border border-white/10 bg-white/5 overflow-hidden shadow-lg">
                            <div class="h-full bg-linear-to-r from-emerald-400 to-cyan-400 rounded-full transition-all duration-300"
                                :style="{ width: progress + '%' }" />
                        </div>
                        <p class="mt-2 text-center text-xs text-white/50 uppercase tracking-[0.2em]">
                            {{ Math.round(progress) }}%
                        </p>
                    </div>

                    <!-- Steps Indicator -->
                    <div class="mb-6 flex gap-2">
                        <div v-for="(warmup, idx) in warmups" :key="idx" class="h-2 flex-1 rounded-full transition-all"
                            :class="idx < step ? 'bg-emerald-400' : idx === step ? 'bg-cyan-400' : 'bg-white/10'" />
                    </div>

                    <!-- Skip Button -->
                    <button @click="skipWarmup"
                        class="mt-auto w-full flex items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-bold text-white/80 transition hover:bg-white/10 hover:text-white active:scale-95">
                        <SkipForward :size="18" />
                        Bỏ qua bài tập
                    </button>
                </section>
            </div>

            <!-- Bottom Stats Bar -->

        </div>
    </div>
</template>