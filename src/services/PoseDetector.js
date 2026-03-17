import { Pose } from "@mediapipe/pose"
import { Camera } from "@mediapipe/camera_utils"
import {
    drawConnectors,
    drawLandmarks
} from "@mediapipe/drawing_utils"

import { useSkeleton, use_analyst, use_analysting } from "./pose_state"
const { get_skeleton } = useSkeleton()
const { get_analyst } = use_analyst()
const { get_analysting, set_analysting } = use_analysting()
import { POSE_CONNECTIONS } from "@mediapipe/pose"
import { usePose } from "./detect_help"
const { drawSafeZone, isInsideSafeZone } = usePose()
let camera = null
let pose = null
let ws = null
let backendData = {
    total: 0,
    good: 0,
    estimate: "",
    state: ""
}
export function startPose(video, canvas, exerciseType, isStarted, emit) {

    const ctx = canvas.getContext("2d")

    ws = new WebSocket(`ws://localhost:8000/websocket/live2?exercise_type=${exerciseType}`)
    ws.onmessage = (event) => {

        try {
            const data = JSON.parse(event.data)
            backendData = data
            // console.log(backendData)
            emit("result", backendData)
        } catch (err) {
            console.log("parse error", err)
        }
    }
    pose = new Pose({
        locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
        }
    })

    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    })

    pose.onResults((results) => {

        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.font = "28px Arial"
        ctx.fillStyle = "yellow"
        ctx.strokeStyle = "black"
        ctx.lineWidth = 3
        const title = exerciseType.toUpperCase()
        if (get_analyst()) {
            ctx.strokeText(`Exercise: ${title}`, 20, 40)
            ctx.fillText(`Exercise: ${title}`, 20, 40)

            ctx.strokeText(`Reps: ${backendData.total}`, 20, 80)
            ctx.fillText(`Reps: ${backendData.total}`, 20, 80)

            ctx.strokeText(`Good: ${backendData.good}`, 20, 120)
            ctx.fillText(`Good: ${backendData.good}`, 20, 120)

            ctx.strokeText(`${backendData.state}`, 20, 160)
            ctx.fillText(`${backendData.state}`, 20, 160)
        }
        if (!results.poseLandmarks) return
        // drawSafeZone(ctx, canvas)

        if (get_skeleton()) {
            drawConnectors(
                ctx,
                results.poseLandmarks,
                POSE_CONNECTIONS,
                { color: "#00FF00", lineWidth: 4 }
            )

            drawLandmarks(
                ctx,
                results.poseLandmarks,
                { color: "#FF0000", lineWidth: 2 }
            )
        }
        const inside = isInsideSafeZone(results.poseLandmarks)

        set_analysting(isStarted.value && inside)

        // ❌ nếu ngoài vùng thì không gửi websocket
        if (!inside || !isStarted.value) return
        const landmarks = results.poseLandmarks.map(p => ({
            x: p.x,
            y: p.y,
            z: p.z,
            visibility: p.visibility
        }))

        if (ws && ws.readyState === 1) {
            ws.send(JSON.stringify({
                landmarks: landmarks
            }))

        }

    })

    camera = new Camera(video, {
        onFrame: async () => {
            await pose.send({ image: video })
        },
        width: 640,
        height: 480
    })

    camera.start()

}

export function stopPose() {

    if (camera) {
        camera.stop()
    }
    if (ws) {
        ws.close()
    }

}