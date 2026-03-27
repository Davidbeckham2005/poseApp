import { onMounted, onUnmounted } from 'vue';
import { Pose } from "@mediapipe/pose";
import { Camera } from "@mediapipe/camera_utils";

// Khai báo biến bên ngoài để dễ quản lý
let pose = null;
let camera = null;

onMounted(async () => {
    const videoElement = document.querySelector(".input_video");

    if (!videoElement) return;

    pose = new Pose({
        locateFile: (file) => {
            // Sử dụng phiên bản cụ thể để tránh lỗi Module.arguments
            return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/${file}`;
        }
    });

    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });

    pose.onResults((results) => {
        // Gửi kết quả về cho game logic hoặc vẽ lên canvas
        if (results.poseLandmarks) {
            console.log("Detecting...");
        }
    });

    camera = new Camera(videoElement, {
        onFrame: async () => {
            await pose.send({ image: videoElement });
        },
        width: 640,
        height: 480
    });

    await camera.start();
});

// QUAN TRỌNG: Dọn dẹp để không bị lỗi khi chuyển trang hoặc save code
onUnmounted(() => {
    if (camera) camera.stop();
    if (pose) pose.close();
});