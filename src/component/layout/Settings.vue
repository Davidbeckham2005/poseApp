<template>
    <div>
        <title_content title="Settings" content="Configure your pose detection preferences">
        </title_content>

        <div class="rounded-2xl w-[75%] bg-gray-700/50 p-5 pr-5 mt-5 pt-5 items-center">
            <Line_under text="Detection Settings"></Line_under>
            <content_click v-for="(setting, key) in settings" :key="key" :title_setting="setting.title" :key_value="key"
                :content_setting="setting.content" :checked_btn="setting.state" @set_active="active">
            </content_click>
        </div>
    </div>
</template>

<script setup>
// component
import Line_under from '../bases/Line_under.vue';
import content_click from '../bases/content_click.vue';
import title_content from '../bases/title_content.vue';
// setting pinia
import { useSetting } from '../../store/setting.store';
import { computed, ref, watch } from 'vue';
const settingStore = useSetting()

// tham so set_active duoc truyen tu component con
const active = (key_value, checked_btn) => {
    console.log(key_value)
    settingStore.setting[key_value] = !checked_btn

}
// array settings se ko hieu qua trong truong hop nay dau, ta nen dung object settings 
// const settings = [
//     { name: "drawing",  },
// ]
const settings = computed(() => ({
    isDrawing: { title: "Show Skeleton Overlay", content: "Display pose keypoints on video", state: settingStore.setting.isDrawing },
    isCheck_view: { title: "Show view", content: "Display view on video", state: settingStore.setting.isCheck_view },
    isAnalyst: { title: "Show Performance Analytics", content: "Display angle measurements, rep counter, and exercise state analysis.", state: settingStore.setting.isAnalyst },
}))

</script>
