<template>
    <div class="coach-container">
        <div ref="animationContainer" class="animation-box"></div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import lottie from "lottie-web"

const animationContainer = ref(null)

onMounted(() => {
    lottie.loadAnimation({
        container: animationContainer.value,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: "/tutorial/pushup_tutorial.json"
    })
})
</script>
