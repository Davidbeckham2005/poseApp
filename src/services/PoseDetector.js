import { Pose } from "@mediapipe/pose"
import { Camera } from "@mediapipe/camera_utils"
import {
    drawConnectors,
    drawLandmarks
} from "@mediapipe/drawing_utils"
import { playSound, useAudio } from "../composable/audio"
const { speak, stopSpeak } = useAudio()
import { useSkeleton, use_analyst, use_analysting } from "./pose_state"
const { get_skeleton } = useSkeleton()
const { get_analyst } = use_analyst()
const { get_analysting, set_analysting } = use_analysting()
import { POSE_CONNECTIONS } from "@mediapipe/pose"
import { usePose } from "./detect_help"
const { drawSafeZone, isInsideSafeZone } = usePose()
import { dataOnRep } from "../composable/help_game"
const { set_data_estimate, get_data_estimate } = dataOnRep()
let lastTotal = -1
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
    down_standard: 0,
    workout_progress: 0,
    target_of_current: 0,
    exercise_type: "",
}
let firstRep = true
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
    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.roundRect(450, 15, 170, 50, 10); // x, y, width, height, radius
    ctx.fill();

    // Vẽ text đồng hồ
    ctx.font = "bold 32px 'Courier New'"; // Font dạng Digital cho giống đồng hồ
    ctx.fillStyle = "#FF4500"; // Màu cam Neon hoặc đỏ cho nổi bật
    ctx.shadowColor = "#FF4500";
    ctx.shadowBlur = 10;

    // Giả sử backendData.current_duration trả về chuỗi "00:05"
    const timeDisplay = backendData.current_duration || "00:00";
    ctx.fillText(timeDisplay, 480, 50);

    // Reset shadow để các nét vẽ sau không bị nhòe
    ctx.shadowBlur = 0;
}
export async function startPose_game2(video, canvas, isStarted, emit, handleResult, handle_game, workoutPlan = []) {
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

    const safePlan = Array.isArray(workoutPlan) && workoutPlan.length > 0
        ? workoutPlan
        : [{ type: "bicep_curls", target: 6 }]
    const planParam = encodeURIComponent(JSON.stringify(safePlan))

    ws = new WebSocket(`ws://localhost:8000/websocket/live_workout?plan=${planParam}`)
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data)
            backendData = data
            if (firstRep && data.total === 1) {
                set_data_estimate(backendData)
                console.log(get_data_estimate())
                firstRep = false
            }
            if (data.total > lastTotal) {
                handleResult("rep")
                lastTotal = data.total
            }
            // console.log(backendData)
            emit("result", backendData)
            if (data.event === "rest_start") {
                // console.log(data.data)
                lastTotal = -1
                firstRep = true
                const second = data.seconds || 10
                startRestCountDown(second)
                const nextEx = data.exercise_type || "bai tiep theo"
                set_data_estimate(backendData)
                handleResult("success")
                speak(`Nghỉ ngơi ${data.seconds || 10} giây, chuẩn bị cho bài tiếp theo"}`)
                currentExerciseTitle = nextEx.toUpperCase()

            }
            if (data.event === "rest_end") {
                // console.log("continue exercise");
                speak("Tiếp tục tập nào!")
                return
            }
            if (data.event === "workout_complete") {
                handle_game()
                emit("finish", data)
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