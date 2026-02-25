<template>
    <div class="flex justify-between">
        <title_content :title="title_setting" :content="content_setting" size_title="text-sm">
        </title_content>
        <input type="checkbox" :checked="checked_btn" @click="emit('set_active', key_value, checked_btn)"
            class="toggle toggle-lg mb-10 text-cyan-400"></input>
    </div>
</template>

<script setup>

const emit = defineEmits(["set_active"])
const props = defineProps({
    key_value: String,
    title_setting: String,
    content_setting: String,
    checked_btn: Boolean,

})
// component
import title_content from './title_content.vue';
</script>
