import { ref, watch } from 'vue'

// ĐƯA BIẾN RA NGOÀI: Để tất cả component dùng chung 1 trạng thái duy nhất
const audioEnabled = ref(true)
let audioUnlocked = false

// Theo dõi biến để hủy speech ngay lập tức khi tắt
watch(audioEnabled, (newVal) => {
    if (!newVal) {
        window.speechSynthesis.cancel()
        console.log('🔈 Audio: Toàn bộ hàng đợi đã được hủy.')
    }
})

export function useAudio() {
    const unlockAudio = () => {
        if (audioUnlocked) return
        const speech = new SpeechSynthesisUtterance("")
        window.speechSynthesis.speak(speech)
        audioUnlocked = true
    }

    const speak = (text) => {
        return new Promise((resolve) => {
            // Kiểm tra trạng thái trước khi bắt đầu
            if (!audioEnabled.value) {
                resolve()
                return
            }

            // QUAN TRỌNG: Hủy các câu nói cũ đang xếp hàng 
            // để tránh việc app đọc "dồn toa" khi tập liên tục
            window.speechSynthesis.cancel()

            const utter = new SpeechSynthesisUtterance(String(text))
            utter.lang = "vi-VN"
            utter.rate = 1.1 // Đọc nhanh hơn một chút để bắt kịp nhịp tập
            utter.pitch = 1

            utter.onend = () => resolve()
            utter.onerror = () => resolve()

            window.speechSynthesis.speak(utter)
        })
    }

    const toggleAudio = () => {
        audioEnabled.value = !audioEnabled.value
    }

    const isAudioEnabled = () => audioEnabled.value

    return { unlockAudio, speak, toggleAudio, isAudioEnabled }
}