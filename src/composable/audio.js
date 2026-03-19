let audioUnlocked = false
import { ref,watch } from 'vue'
export function useAudio() {
    const audioEnabled = ref(true)
    watch(audioEnabled, (newVal) => {
        if (!newVal) {
            window.speechSynthesis.cancel()
            console.log('Audio disabled, speech cancelled')
        }
    })
    const unlockAudio = () => {
        if (audioUnlocked) return
        // phát 1 speech rỗng để mở khóa audio
        const speech = new SpeechSynthesisUtterance("")
        window.speechSynthesis.speak(speech)
        audioUnlocked = true
    }
    const speak = (text) => {
        return new Promise((resolve) => {
            if (!audioEnabled.value) {
                resolve()
                return
            }
            const utter = new SpeechSynthesisUtterance(String(text))
            utter.lang = "vi-VN"
            utter.rate = 1
            utter.pitch = 1

            utter.onend = () => resolve()
            utter.onerror = () => resolve()

            speechSynthesis.speak(utter)
        })
    }
    //  bật/tắt âm thanh
    const toggleAudio = () => {
        audioEnabled.value = !audioEnabled.value
        return audioEnabled
    }
    // kiểm tra trạng thái âm thanh
    const isAudioEnabled = () => {
        return audioEnabled.value
    }
    return { unlockAudio, speak, toggleAudio, isAudioEnabled }
}



