<template>
    <div class="flex flex-col items-center gap-6">
        <!-- CAMERA CONTAINER -->
        <div class="relative w-[640px] h-[480px] rounded-2xl overflow-hidden bg-slat-900 shadow-2xl">
            <!-- video -->
            <video ref="videoRef" class="absolute inset-0 w-full h-full object-cover scale-x-[-1]" autoplay
                playsinline />
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

        <!-- TIPS DISPLAY -->
        <div v-if="tutorial_message" class="mt-4 p-4 bg-gray-800 text-white rounded-lg shadow-md">
            <p class="text-center text-lg font-semibold">{{ tutorial_message }}</p>
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
// props 
const props = defineProps({ exercise_type: String, currentHp: Number })
const emit = defineEmits(['result', 'finish'])

// import
import { computed, ref, watch } from "vue"
import { startPose, stopPose } from "../../../services/PoseDetector"
import { usePose } from "../../../services/detect_help"
import { exercises_data } from "../../../constants/exercise"
import { useAudio } from '../../../composable/audio'
const { speak } = useAudio()

// khai bao bien
const { isInside } = usePose()
const videoRef = ref(null)
const canvasRef = ref(null)
const isStarted = ref(false)
const current_exercise_type = ref(null)
let tipsInterval = null
const tutorial_message = ref("")
/* trạng thái người dùng trong safe zone */
const inside = computed(() => { return isInside.value })

// trạng thái để kiểm soát việc nói cảnh báo
const isSpeakingWarning = ref(false)
let warningInterval = null

// trạng thái của bài tập được chọn
watch(() => props.exercise_type, (newValue) => {
    current_exercise_type.value = newValue
})

// theo dõi hp của quái
watch(() => props.currentHp, (newValue) => {
    if (newValue <= 0) {
        startCamera()
        emit('finish')
    }
})

// start camera và bắt đầu bài tập
const startCamera = () => {
    isStarted.value = true
    console.log('Starting pose detection for exercise type:', current_exercise_type.value)
    startPose(videoRef.value, canvasRef.value, current_exercise_type.value, isStarted)
    startRotationTips()
}

//  strop camera và dừng bài tập
const stopCamera = () => {
    isStarted.value = false
    stopPose()
}

// cảnh báo khi người dùng không đứng trong safe zone
const warning = computed(() => {
    return isStarted.value && !inside.value
})

// Theo dõi trạng thái cảnh báo và thông báo bằng giọng nói
watch(warning, (newValue) => {
    if (newValue) {
        if (tipsInterval) clearInterval(tipsInterval) // Dừng nói tips khi có cảnh báo
        if (!warningInterval) {

            warningInterval = setInterval(() => {
                speak("Vui lòng đứng vào khung tập để tiếp tục bài tập")
            }, 2000) // Lặp lại cảnh báo mỗi 5 giây
        }
    } else {
        clearInterval(warningInterval)
        warningInterval = null
        startRotationTips() // Tiếp tục nói tips khi cảnh báo kết thúc
    }
})

// tính toán và hiển thị tips bài tập
const exercise_tips = computed(() => { return exercises_data.find(e => e.type === current_exercise_type.value)?.tips })
const startRotationTips = async () => {
    if (warning.value) return
    // Không bắt đầu tips nếu đang có cảnh báo
    if (!isStarted.value) return
    if (tipsInterval) clearInterval(tipsInterval)
    const tips = exercise_tips.value || []
    if (tips.length === 0) return

    let index = 0
    // Hiển thị câu đầu tiên ngay lập tức
    tutorial_message.value = tips[0]
    await speak(tutorial_message.value)
    tipsInterval = setInterval(async () => {
        index = (index + 1) % tips.length
        tutorial_message.value = tips[index]
        await speak(tips[index])
    }, 6000)
}
</script>