<template>
    <div class="flex justify-between">
        <title_content :title="title_setting" :content="content_setting" size_title="text-sm">
        </title_content>
        <input type="checkbox" :checked="checked_btn" v-model="isClick" class="toggle text-cyan-400 toggle-lg mb-10">{{
            checked_btn }}</input>
    </div>
</template>

<script setup>
const props = defineProps({
    title_setting: String,
    content_setting: String,
    checked_btn: Boolean
})
// component
import title_content from './title_content.vue';
import { ref, watch } from 'vue';
// su ly click
// const isClick = ref(false)
// watch(isClick, (newValue) => {
// console.log(newValue)
//     console.log(isClick.value)
// }
// )
</script>
