import {
    drawConnectors,
    drawLandmarks
} from "@mediapipe/drawing_utils"

import { POSE_CONNECTIONS } from "@mediapipe/pose"

export function drawSkeleton(ctx, landmarks) {

    drawConnectors(
        ctx,
        landmarks,
        POSE_CONNECTIONS,
        { color: "#00FF00", lineWidth: 4 }
    )

    drawLandmarks(
        ctx,
        landmarks,
        { color: "#FF0000", lineWidth: 2 }
    )
    
}
