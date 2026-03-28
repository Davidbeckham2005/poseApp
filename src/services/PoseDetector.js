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
    state: "",
    origin: "",
    good_standard: 0,
    bad_standard: 0,
    up_standard: 0,
    workout_progress: 0,
    target_of_current: 0,
    exercise_type: "",
}
let restime = 0
let restInterval = null
let nextExercise = "";
const startRestCountDown = (seconds) => {
    restime = seconds
    if (restInterval) clearInterval(restInterval)

    restInterval = setInterval(() => {
        restime -= 1
        if (restime <= 0) {
            clearInterval(restInterval)
            restInterval = null
        }
    }, 1000)
}
const drawRestTimeOverlay = (ctx, canvas, seconds, nextExercise) => {
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.shadowBlur = 0;

    ctx.font = "bold 48px Arial";
    ctx.fillStyle = "#00FF00";
    ctx.textAlign = "center";
    ctx.fillText(`CHUẨN BỊ`, canvas.width / 2, canvas.height / 2 - 100);

    ctx.font = "30px Arial"
    ctx.filelStyle = "white"
    ctx.fillText(`Bài tiếp theo: ${nextExercise}`, canvas.width / 2, canvas.height / 2 - 40)

    ctx.font = "bold 120px Arial"
    if (seconds <= 3) {
        ctx.fillStyle = "red"
        ctx.shadowColor = "red";
    } else {
        ctx.fillStyle = "yellow"
    }
    ctx.fillText(seconds, canvas.width / 2, canvas.height / 2 + 80)

    ctx.textAlign = "left"

}
    const drawHUB = (ctx, backendData) => {
        ctx.font = "bold 28px Arial";
        ctx.shadowBlur = 4;
        ctx.shadowColor = "black";

        ctx.fillStyle = "#00BFFF";
        ctx.fillText(`Bài tập: ${backendData.exercise_type}`, 20, 40);

        ctx.fillStyle = "yellow"
        ctx.fillText(`Reps: ${backendData.total}/${backendData.target_of_current || 0}`, 20, 80)

        if (backendData.workout_progress) {
            ctx.fillStyle = "#00FF00";
            ctx.fillText(`Tiến độ: ${backendData.workout_progress}`, 20, 120)
        }

        ctx.fillStyle = "white";
        ctx.fillText(`Trạng thái: ${backendData.state}`, 20, 160)
    }
    export async function startPose_game2(video, canvas, exerciseType, isStarted, emit) {
        if (camera) {
            await camera.stop();
            camera = null;
        }
        if (pose) {
            await pose.close();
            pose = null;
        }
        if (ws) {
            ws.close();
            ws = null;
        }
        const ctx = canvas.getContext("2d")

        ws = new WebSocket(`ws://localhost:8000/websocket/live_workout`)
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                backendData = data
                // console.log(backendData)
                emit("result", backendData)
                if (data.event === "rest_start") {
                    const second = data.seconds || 10
                    startRestCountDown(second)
                    const nextEx = data.exercise_type || "bai tiep theo"
                    currentExerciseTitle = nextEx.toUpperCase()

                }
                if (data.event === "rest_end") {
                    console.log("continue exercise");
                    return
                }
                if (data.event === "workout_complete") {
                    console.log("Chúc mừng! Bạn đã hoàn thành chuỗi bài tập.");
                    return
                }
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

            if (restime > 0) {
                drawRestTimeOverlay(ctx, canvas, restime, nextExercise)
            } else {
                drawHUB(ctx, backendData)
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
    export async function startPose(video, canvas, exerciseType, isStarted, emit) {
        if (camera) {
            await camera.stop();
            camera = null;
        }
        if (pose) {
            await pose.close();
            pose = null;
        }
        if (ws) {
            ws.close();
            ws = null;
        }
        const ctx = canvas.getContext("2d")

        ws = new WebSocket(`ws://localhost:8000/websocket/live2?exercise_type=${exerciseType}`)
        ws.onmessage = (event) => {

            try {
                const data = JSON.parse(event.data)
                backendData = data
                console.log(backendData)
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