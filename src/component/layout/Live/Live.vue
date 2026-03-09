<template>
    <div class="flex flex-col">
        <div
            class="relative w-full flex flex-col items-center p-4 rounded-3xl justify-between overflow-hidden bg-black border border-white/20 shadow-2xl">
            <video ref="videoRef" autoplay playsinline class="w-full -scale-x-100 rounded-3xl mb-2"></video>
            <div v-if="statusMessage || countdown"
                class="absolute inset-0 flex items-center justify-center bg-black/40 pointer-events-none">

                <div
                    class="text-center p-3 rounded-2xl bg-black/30 backdrop-blur border border-white/20 items-center flex">
                    <h1 v-if="countdown" class="text-5xl font-medium text-white">
                        {{ countdown }}
                    </h1>
                    <p v-else class="text-xl font-medium text-white uppercase tracking-widest">
                        {{ statusMessage }}
                    </p>
                </div>
            </div>

            <div>
                <div class="space-x-3">
                    <button :disabled="!exercise_type || stream" @click="startCamera"
                        class="rounded-lg btn btn-error">start</button>
                    <button :disabled="start_analyst || !stream?.active" @click="stopCamera"
                        class="rounded-lg btn btn-active">stop</button>
                    <button :disabled="start_analyst || !stream?.active" @click="handle_analyst"
                        class="rounded-lg btn btn-info">start
                        Analyst </button>
                    <button :disabled="!start_analyst" @click="stopAnalyst" class="rounded-lg btn btn-info">stop
                        Analyst</button>
                </div>
                <!-- <button class="btn btn-info" @click="emit('result', { total: 0, good: 0, estimate: '' })"></button>
                <button class="btn btn-info" @click="emit('result', { total: 3, good: 2, estimate: 'good' })"></button>
                <button class="btn btn-accent" @click="emit('result', { total: 4, good: 3, estimate: 'bad' })"></button> -->
            </div>
        </div>
        <p v-if="start_analyst" class="text-lg font-medium text-center text-white uppercase tracking-widest">
            {{ tutorial_message }}
        </p>
        <!-- <div class="w-40 border border-amber-300 rounded-3xl"></div> -->
    </div>
</template>
<script setup>
const emit = defineEmits(['result', 'is_analyst'])
const props = defineProps({ exercise_type: String })
import { ref, onUnmounted, onMounted, toRaw, watch } from 'vue'

const videoRef = ref(null)
const start_analyst = ref(false)
const old_data = ref('')
const current_exercise = ref()


let stream = ref(null)
let ws = null

watch(() => props.exercise_type, (newValue) => {
    current_exercise.value = newValue
})
const connect = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close()
    }
    ws = new WebSocket(`ws://localhost:8000/websocket/live?exercise_type=${current_exercise.value}`)
    ws.onopen = () => {
        console.log("connected with exercise: ", current_exercise.value)
    }
    ws.onmessage = (e) => {
        const newData = e.data
        const data = JSON.parse(e.data)
        if (newData != old_data.value) {
            emit('result', data)
        }
        old_data.value = newData
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
    console.log(ws.readyState)
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
const exercise_tips = {
    squat: [
        "Giữ lưng thẳng, không để cong lưng",
        "Dồn trọng tâm vào gót chân",
        "Hạ mông xuống thấp nhất có thể",
        "Đừng để đầu gối quá mũi chân",
        "Hít vào khi xuống, thở ra khi lên"
    ],
    pushup: [
        "Giữ cơ thể thành một đường thẳng",
        "Không để mông quá cao hoặc quá thấp",
        "Mở rộng ngực khi hạ người xuống",
        "Gồng chặt cơ bụng khi thực hiện",
        "Khuỷu tay khép vào gần thân người"
    ],
    plank: [
        "Giữ đầu, lưng, chân thẳng hàng",
        "Không nín thở, hãy hít thở đều",
        "Gồng chặt cơ bụng và cơ mông",
        "Mắt nhìn xuống sàn, đừng ngước lên",
        "Cố gắng giữ vững tư thế, đừng rung lắc"
    ]
}

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
const startRotationTips = (type) => {
    if (!start_analyst.value) return
    // Xóa interval cũ nếu có
    if (tipsInterval) clearInterval(tipsInterval)

    const tips = exercise_tips[type] || []
    if (tips.length === 0) return

    let index = 0
    // Hiển thị câu đầu tiên ngay lập tức
    tutorial_message.value = tips[0]

    // Cứ mỗi 6 giây đổi một câu khác
    tipsInterval = setInterval(() => {
        index = (index + 1) % tips.length
        tutorial_message.value = tips[index]
    }, 6000)
}
</script>
