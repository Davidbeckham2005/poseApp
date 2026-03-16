import { ref } from 'vue'
const isInside = ref(false)
export function usePose() {
    function isInsideSafeZone(landmarks, canvas) {

        const hipLeft = landmarks[23]
        const hipRight = landmarks[24]

        const centerX = (hipLeft.x + hipRight.x) / 2
        const centerY = (hipLeft.y + hipRight.y) / 2

        const width = 0.5
        const height = 0.7

        const minX = 0.5 - width / 2
        const maxX = 0.5 + width / 2
        const minY = 0.5 - height / 2
        const maxY = 0.5 + height / 2

        const Inside = (centerX > minX &&
            centerX < maxX &&
            centerY > minY &&
            centerY < maxY)
        isInside.value = Inside
        return Inside
    }
    function drawSafeZone(ctx, canvas) {

        const width = canvas.width * 0.5
        const height = canvas.height * 0.7

        const x = (canvas.width - width) / 2
        const y = (canvas.height - height) / 2

        ctx.save()

        ctx.strokeStyle = "rgba(0,255,0,0.8)"
        ctx.lineWidth = 4
        ctx.setLineDash([10, 10])

        ctx.strokeRect(x, y, width, height)

        ctx.restore()

    }
    return { drawSafeZone, isInsideSafeZone, isInside }
}

