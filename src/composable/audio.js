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
        if (!audioUnlocked) return
        // window.speechSynthesis.cancel()
        const speech = new SpeechSynthesisUtterance(text)
        speech.lang = "vi-VN"
        speech.rate = 1
        window.speechSynthesis.speak(speech)
    }
    return { unlockAudio, speak }
}



