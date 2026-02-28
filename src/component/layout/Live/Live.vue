<template>
    <div class="flex flex-row">
        <div
            class="w-full flex flex-col items-center p-4 rounded-3xl justify-between overflow-hidden bg-black border border-slate-800 shadow-2xl h-auto">
            <video ref="videoRef" autoplay playsinline class="w-full -scale-x-100 rounded-3xl mb-2"></video>
            <div>
                <div class="space-x-3">
                    <button @click="startCamera" class="rounded-lg btn btn-error">start</button>
                    <button @click="stopCamera" class="rounded-lg btn btn-active">stop</button>
                    <button @click="startAnalyst" class="rounded-lg btn btn-info">start Analyst</button>
                </div>
            </div>
        </div>
        <div class="w-40 border border-amber-300 rounded-3xl"></div>
    </div>
    <!-- <div class="grid grid-cols-3 gap-6 space-y-2">
        <div v-for="i in 3" :key="i"
            class="bg-gray-900/40 border border-gray-800 p-5 rounded-xl hover:border-gray-700 transition cursor-pointer">
            <div class="bg-gray-800 w-10 h-10 rounded flex items-center justify-center mb-4">
                <VideoIcon class="w-5 h-5 text-gray-400" />
            </div>
            <h4 class="font-medium text-white">Sample Video {{ i }}</h4>
            <p class="text-sm text-gray-500 mt-1">{{ ['Squat Exercise', 'Push-up Demo', 'Plank Hold'][i
                - 1]
                }}</p>
        </div>
    </div>
    <div class="bg-gray-900/20 border border-gray-800 rounded-xl p-6">
        <h4 class="font-semibold text-white mb-4">Upload Guidelines</h4>
        <ul class="space-y-2 text-sm text-gray-400">
            <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                Ensure the subject is clearly visible in the frame</li>
            <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                Good lighting improves pose detection accuracy</li>
            <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                Avoid cluttered backgrounds for best results</li>
            <li class="flex items-center"><span class="w-1.5 h-1.5 bg-cyan-500 rounded-full mr-3"></span>
                Supported exercises: squat, push-up, plank, lunge, etc.</li>
        </ul>
    </div> -->
</template>

<script setup>

import { ref, onUnmounted, onMounted } from 'vue'
const videoRef = ref(null)
const start_analys = ref(false)
let stream = null
const startCamera = async () => {
    try {
        if (stream) stopCamera()
        stream = await navigator.mediaDevices.getUserMedia(
            {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    frameRate: { ideal: 30 }
                },
                audio: false
            }
        )
        videoRef.value.srcObject = stream
    } catch (error) {
        console.log(error)
    }
}
const stopCamera = () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop())
        if (videoRef.value) {
            videoRef.value.srcObject = null
        }
        stream = null
    }
    return
}
const handle_keydown = (even) => {
    if (even.key.toLowerCase() === 'q') {
        stopCamera()
    }
}
onMounted(() => window.addEventListener('keydown', handle_keydown))
onUnmounted(() => {
    window.removeEventListener('keydown', handle_keydown)
    stopCamera()
})

const ws = new WebSocket("ws://localhost:8000/ws")
ws.onopen = () => {
    console.log("connected")
    sendData()
}
ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    console.log(data)
    if (start_analys.value)
        sendData()
}
const canvas = document.createElement('canvas')
const ctx = canvas.getContext('2d')
function sendData() {
    const video = videoRef.value
    if (ws.readyState !== WebSocket.OPEN || !video) {
        return
    }
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.toBlob((blob) => {
        if (blob && ws.readyState === WebSocket.OPEN) {
            console.log(blob)
            ws.send(blob);
        }
    }, 'image/jpeg', 0.6);
}
const startAnalyst = () => {
    start_analys.value = true

    sendData()
}
</script>
