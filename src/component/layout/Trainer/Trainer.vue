<template>
    <div class="coach-container">
        <div ref="animationContainer" class="animation-box"></div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import lottie from "lottie-web"
const props = defineProps({ path_json: String })
const animationContainer = ref(null)

onMounted(() => {
    lottie.loadAnimation({
        container: animationContainer.value,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: `${props.path_json}.json`
        // path: `/Monster/${props.path_json}.json`
    })
})
</script>
