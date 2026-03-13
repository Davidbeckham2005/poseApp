<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { Timer, Activity, SkipForward } from "lucide-vue-next"
import { useAudio } from "../../../composable/audio"
const { unlockAudio } = useAudio()
import { Use_is_warmup } from "../../../composable/help_game"
import Trainer from "../Trainer/Trainer.vue"

const { get_state_warmup, set_state_warmup } = Use_is_warmup()
const { speak } = useAudio()
const warmups = [
    { name: "Dãn vai", time: 10, speak_voice: "Dãn vai", path: "/tutorial/Shoulder Stretch" },
    { name: "Dũi chân", time: 20, speak_voice: "Dũi chân", path: "/tutorial/Single Leg Hip Rotation" },
    { name: "Squat nhẹ", time: 30, speak_voice: "sờ quáp nhẹ", path: "/tutorial/Squat Reach" },
    { name: "Jump tại chỗ", time: 20, speak_voice: "dăm tại chổ", path: "/tutorial/Jumping Jack" }
]

const step = ref(0)
const timeLeft = ref(warmups[0].time)
let timer = null

const current = computed(() => warmups[step.value])

const progress = computed(() => {
    return ((current.value.time - timeLeft.value) / current.value.time) * 100
})

function nextStep() {
    step.value++
    if (step.value < warmups.length) {
        speak(`Bắt đầu ${warmups[step.value].speak_voice}`)
        timeLeft.value = warmups[step.value].time
    } else {
        clearInterval(timer)
        set_state_warmup(false)
    }
}

onMounted(() => {
    timer = setInterval(() => {
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
    speechSynthesis.cancel()
})
</script>

<template>
    <div @click.once="unlockAudio" class="flex items-center justify-center bg-gray-900 text-white">

        <div class="w-[420px] bg-gray-800 rounded-2xl p-8 shadow-xl space-y-6">
            <Trainer :path_json="warmups[step].path" :key="step"></Trainer>
            <div class="text-center space-y-2">
                <!-- <Activity class="mx-auto text-orange-400" :size="40" /> -->
                <h1 class="text-2xl font-bold">Khởi động - {{ current.name }}</h1>
                <p class="text-gray-400 text-sm">
                    Chuẩn bị cơ thể trước trận chiến
                </p>
            </div>

            <!-- exercise -->
            <div class="text-center">
                <div class="flex items-center justify-center text-orange-400">
                    <Timer :size="20" />
                    <span class="text-lg font-bold">
                        {{ timeLeft }}s
                    </span>
                </div>
            </div>

            <!-- progress -->
            <div class="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full dark:bg-orange-400 transition-all" :style="{ width: progress + '%' }" />
            </div>

            <!-- step -->
            <div class="text-center text-sm text-gray-400">
                Bài {{ step + 1 }} / {{ warmups.length }}
            </div>

            <!-- skip -->
            <button @click="nextStep"
                class="w-full flex items-center justify-center gap-2 bg-gray-700 hover:bg-gray-600 transition rounded-xl py-2">
                <SkipForward :size="18" />
                Bỏ qua
            </button>
        </div>
    </div>
</template>