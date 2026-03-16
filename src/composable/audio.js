let audioUnlocked = false
export function useAudio() {
    const unlockAudio = () => {
        if (audioUnlocked) return
        // phát 1 speech rỗng để mở khóa audio
        const speech = new SpeechSynthesisUtterance("")
        window.speechSynthesis.speak(speech)
        audioUnlocked = true
    }
    const speak = (text) => {
        return new Promise((resolve) => {
            const utter = new SpeechSynthesisUtterance(String(text))
            utter.lang = "vi-VN"
            utter.rate = 1
            utter.pitch = 1

            utter.onend = () => resolve()
            utter.onerror = () => resolve()

            speechSynthesis.speak(utter)
        })
    }
    return { unlockAudio, speak }
}



