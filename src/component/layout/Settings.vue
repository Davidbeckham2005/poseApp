<template>
    <div>
        <title_content title="Settings" content="Configure your pose detection preferences">
        </title_content>

        <div class="rounded-2xl w-[80%] bg-gray-700/50 p-5 pr-5 mt-5 pt-5 items-center">
            <Line_under text="Detection Settings"></Line_under>
            <content_click v-for="setting in settings" :title_setting="setting.title" :content_setting="setting.content"
                :checked_btn="setting.state">
            </content_click>

        </div>
    </div>
</template>

<script setup>
// component
import Line_under from '../bases/Line_under.vue';
import content_click from '../bases/content_click.vue';
import title_content from '../bases/title_content.vue';

// object settings
const settings = [
    { name: "drawing", title: "Show Skeleton Overlay", content: "Display pose keypoints on video", state: false },
]
</script>
