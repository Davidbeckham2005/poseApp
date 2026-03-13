<template>
    <div class="flex flex-col w-full max-w-4xl mx-auto font-sans text-slate-200">
        <div
            class="relative w-full aspect-video rounded-3xl overflow-hidden bg-slate-950 border border-white/10 shadow-2xl group">

            <img v-if="start_analyst && frame" :src="frame" class="absolute inset-0 w-full h-full object-cover"
                alt="AI Processed Frame">
            <video v-show="!frame || !start_analyst" ref="videoRef" autoplay playsinline
                class="w-full h-full object-cover -scale-x-100 transition-opacity duration-500"
                :class="{ 'opacity-40': !stream, 'opacity-100': stream }"></video>

            <Transition name="fade">
                <div v-if="statusMessage || countdown"
                    class="absolute inset-0 z-20 flex items-center justify-center bg-black/60 backdrop-blur-[2px]">
                    <div class="text-center p-8">
                        <Transition name="zoom" mode="out-in">
                            <h1 v-if="countdown" :key="countdown"
                                class="text-9xl font-black text-white drop-shadow-[0_0_20px_rgba(255,255,255,0.5)]">
                                {{ countdown }}
                            </h1>
                            <div v-else :key="statusMessage" class="space-y-4">
                                <div
                                    class="inline-block px-6 py-2 rounded-full bg-blue-500/20 border border-blue-400/50 text-blue-300 text-xs uppercase tracking-[0.3em] animate-pulse">
                                    System Status
                                </div>
                                <p class="text-3xl font-bold text-white max-w-md mx-auto leading-tight">
                                    {{ statusMessage }}
                                </p>
                            </div>
                        </Transition>
                    </div>
                </div>
            </Transition>

            <div
                class="absolute bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 px-6 py-3 rounded-2xl bg-black/40 backdrop-blur-xl border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-30">

                <button v-if="!stream" @click="startCamera" :disabled="!exercise_type"
                    class="flex items-center gap-2 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 disabled:bg-slate-700 text-white rounded-xl font-semibold transition-all active:scale-95">
                    <div class="w-2 h-2 rounded-full bg-white animate-ping" />
                    Mở Camera
                </button>

                <button v-else @click="stopCamera" :disabled="start_analyst"
                    class="px-5 py-2.5 bg-white/10 hover:bg-red-500/20 text-white rounded-xl font-semibold transition-all border border-white/5 hover:border-red-500/50">
                    Tắt Camera
                </button>

                <div class="w-[1px] h-6 bg-white/10 mx-2"></div>

                <button v-if="!start_analyst" @click="handle_analyst" :disabled="!stream?.active"
                    class="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-xl font-semibold shadow-lg shadow-blue-900/20 transition-all active:scale-95">
                    Bắt đầu Phân tích
                </button>

                <button v-else @click="stopAnalyst"
                    class="px-6 py-2.5 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-semibold shadow-lg shadow-orange-900/20 transition-all">
                    Dừng Phân tích
                </button>
            </div>
        </div>

        <Transition name="slide-up">
            <div v-if="start_analyst" class="mt-8">
                <div
                    class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-500/10 to-transparent border border-orange-500/20 p-5 flex items-start gap-4">
                    <div class="p-3 rounded-xl bg-orange-500/20 text-orange-400 shadow-inner">
                        <Lightbulb :size="24" />
                    </div>
                    <div class="flex-1">
                        <h4 class="text-orange-400 font-bold text-xs uppercase tracking-widest mb-1">Hướng dẫn
                        </h4>
                        <p class="text-orange-100 text-lg leading-relaxed italic">
                            "{{ tutorial_message }}"
                        </p>
                    </div>
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-orange-500/5 rounded-full blur-2xl"></div>
                </div>
            </div>
        </Transition>
    </div>
</template>
<script setup>
const emit = defineEmits(['result', 'is_analyst', 'finish'])
const props = defineProps({ exercise_type: String, currentHp: Number })
const frame = ref("")
import { ref, onUnmounted, onMounted, watch, computed } from 'vue'
import { Lightbulb } from 'lucide-vue-next'
const videoRef = ref(null)
const start_analyst = ref(false)
const old_data = ref('')
const current_exercise = ref()
let stream = ref(null)
let ws = null
let lastUrl = null

watch(() => props.exercise_type, (newValue) => {
    current_exercise.value = newValue
    console.log(current_exercise.value)
})
const connect = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close()
    }
    ws = new WebSocket(`ws://localhost:8000/websocket/live?exercise_type=${current_exercise.value}`)
    ws.onopen = () => {
        console.log("connected with exercise: ", current_exercise.value)
    }
    ws.binaryType = "arraybuffer"
    ws.onmessage = (e) => {
        // console.log(e.data)
        const buffer = new Uint8Array(e.data)
        if (buffer.length < 4) return
        const jsonLength =
            (buffer[0] << 24) |
            (buffer[1] << 16) |
            (buffer[2] << 8) |
            buffer[3]

        const jsonBytes = buffer.slice(4, 4 + jsonLength)
        const frameBytes = buffer.slice(4 + jsonLength)
        const jsonString = new TextDecoder().decode(jsonBytes)
        const data = JSON.parse(jsonString)
        old_data.value = data
        const blob = new Blob([frameBytes], { type: "image/jpeg" })
        if (lastUrl) {
            URL.revokeObjectURL(lastUrl)
        }
        lastUrl = URL.createObjectURL(blob)
        frame.value = lastUrl

        if (data != old_data.value) {
            emit('result', data)
        }
        old_data.value = data
    }
}

const startCamera = async () => {
    try {
        stream.value = await navigator.mediaDevices.getUserMedia(
            {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    frameRate: { ideal: 30 }
                },
                audio: false
            }
        )
        videoRef.value.srcObject = stream.value
    } catch (error) {
        console.log(error)
    }
}
const stopCamera = () => {
    if (stream.value) {
        stream.value.getTracks().forEach(track => track.stop())
        if (videoRef.value) {
            videoRef.value.srcObject = null
        }
        stream.value = null
    }
    return
}
const handle_keydown = (even) => {
    if (even.key.toLowerCase() === 'q') {
        stopCamera()
        ws.close()
    }
}
onMounted(() => window.addEventListener('keydown', handle_keydown))
onUnmounted(() => {
    window.removeEventListener('keydown', handle_keydown)
    if (stream) stopCamera()
    if (ws && ws.readyState !== WebSocket.CLOSED) {
        console.log("Closed websocket")
        ws.close()
    }
    clearInterval(tipsInterval)
})

function loop() {
    if (!start_analyst.value) return
    sendData()
    requestAnimationFrame(loop)
}
const canvas = document.createElement('canvas')
const ctx = canvas.getContext('2d')

// ham send data
const sendData = () => {
    const video = videoRef.value
    // vi sao ws ready state o day la connectting nghia la 0, nhung co ve nhu ko senddata  phai la 1 thi moi send duoc dung k oke
    if (ws.readyState !== WebSocket.OPEN || !video) {
        return
    }
    const scale = 640 / video.videoWidth
    canvas.width = 640;
    canvas.height = video.videoHeight * scale;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.toBlob((blob) => {
        if (!blob || ws.readyState !== WebSocket.OPEN) {
            return
        }
        ws.send(blob)
    }, 'image/jpeg', 0.4);
}

watch(() => props.currentHp, (newValue) => {
    if (newValue <= 0) {
        stopAnalyst()
        emit('finish')
    }
})
// message and countdown
const statusMessage = ref('') // Lưu dòng chữ thông báo
const countdown = ref(null)   // Lưu số giây đếm ngược (3, 2, 1)
const tutorial_message = ref('')
// Hàm hỗ trợ delay (đợi)
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
const startAnalyst = async () => {
    connect()
    startRepare()
    start_analyst.value = true
    loop()
    startRotationTips(props.exercise_type)
}
const stopAnalyst = () => {
    start_analyst.value = false
    emit('is_analyst', start_analyst.value)
    ws.close()
}
const handle_analyst = () => {
    startAnalyst()
    emit('is_analyst', start_analyst.value)
}
import { exercises_data } from '../../../constants/exercise'
const exercise_tips = computed(() => { return exercises_data.find(e => e.type === current_exercise.value).tips })
watch(start_analyst, () => {
    if (!start_analyst.value) {
        speechSynthesis.cancel()
        clearInterval(tipsInterval)
    }
})
let tipsInterval = null
const startRepare = async () => {
    statusMessage.value = "Đang khởi động hệ thống AI..."
    await delay(1500)

    statusMessage.value = "Vui lòng đứng xa camera khoảng 2-3 mét để thấy toàn thân"
    await delay(3000)
    statusMessage.value = "Chuẩn bị..."
    countdown.value = 3

    while (countdown.value > 0) {
        await delay(1000)
        countdown.value--
    }

    countdown.value = null
    statusMessage.value = "BẮT ĐẦU!"

    await delay(2000)
    statusMessage.value = ""
}
import { useAudio } from '../../../composable/audio'
const { speak } = useAudio()
const startRotationTips = () => {
    if (!start_analyst.value) return
    // Xóa interval cũ nếu có
    if (tipsInterval) clearInterval(tipsInterval)

    const tips = exercise_tips.value || []
    if (tips.length === 0) return

    let index = 0
    // Hiển thị câu đầu tiên ngay lập tức
    tutorial_message.value = tips[0]

    // Cứ mỗi 6 giây đổi một câu khác
    tipsInterval = setInterval(() => {
        index = (index + 1) % tips.length
        speak(tips[index])
        tutorial_message.value = tips[index]
    }, 6000)
}
</script>
<style scoped>
/* Animations cho UX mượt mà */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.zoom-enter-active,
.zoom-leave-active {
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.zoom-enter-from {
    transform: scale(0.5);
    opacity: 0;
}

.zoom-leave-to {
    transform: scale(1.2);
    opacity: 0;
}

.slide-up-enter-active {
    transition: all 0.5s ease-out;
}

.slide-up-enter-from {
    transform: translateY(20px);
    opacity: 0;
}
</style>