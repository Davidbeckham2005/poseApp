import { Pose } from "@mediapipe/pose"
import { Camera } from "@mediapipe/camera_utils"

const videoElement = document.querySelector(".input_video")

const pose = new Pose({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
    }
})

pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
})

pose.onResults((results) => {
    console.log(results.poseLandmarks)
})

const camera = new Camera(videoElement, {
    onFrame: async () => {
        await pose.send({ image: videoElement })
    },
    width: 640,
    height: 480
})

camera.start()