<template>
    <div>
        <title_content title="Settings" content="Configure your pose detection preferences">
        </title_content>

        <div class="rounded-2xl w-[75%] bg-gray-700/50 p-5 pr-5 pt-5 items-center">
            <Line_under text="Detection Settings"></Line_under>
            <content_click v-for="(setting, key) in settings_detect" :key="key" :title_setting="setting.title"
                :key_value="key" :content_setting="setting.content" :checked_btn="setting.state" @set_active="active">
            </content_click>

        </div>
        <div class="rounded-2xl w-[75%] bg-gray-700/50 p-5 pr-5 mt-5 pt-5 items-center">
            <Line_under text="Analyst settings"></Line_under>
            <content_click v-for="(setting, key) in setting_analyst" :key="key" :title_setting="setting.title"
                :key_value="key" :content_setting="setting.content" :checked_btn="setting.state" @set_active="active">
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
    if (key_value === 'isAnalyst') {
        settingStore.setting['isAnalyst'] = !checked_btn
        settingStore.setting['Analyst_FPS'] = !checked_btn
        settingStore.setting['Analyst_state'] = !checked_btn
        settingStore.setting['Analyst_estimate'] = !checked_btn
        settingStore.setting['Analyst_count'] = !checked_btn
        settingStore.setting['Analyst_count_good'] = !checked_btn

    }
    else
        settingStore.setting[key_value] = !checked_btn

}
// array settings se ko hieu qua trong truong hop nay dau, ta nen dung object settings 
// const settings = [
//     { name: "drawing",  },
// ]
const settings_detect = computed(() => ({
    isDrawing: { title: "Display Skeleton Overlay", content: "Display pose keypoints on video", state: settingStore.setting.isDrawing },
    isCheck_view: { title: "Display layout", content: "Switch between horizontal and vertical view", state: settingStore.setting.isCheck_view },
}))
const setting_analyst = computed(() => ({
    isAnalyst: { title: "Display Analytics", content: "Display rep counter, and exercise state analysis.", state: settingStore.setting.isAnalyst },
    Analyst_FPS: { title: "Display FPS", content: "Display real-time FPS", state: settingStore.setting.Analyst_FPS },
    Analyst_state: { title: "Display Exercise State", content: "Display current movement status (e.g., Up/Down/Hold)", state: settingStore.setting.Analyst_state },
    Analyst_count: { title: "Display Count", content: "Display total number of repetitions performed", state: settingStore.setting.Analyst_count },
    Analyst_count_good: { title: "Display good count", content: "Display the count of correctly movements", state: settingStore.setting.Analyst_count_good },
    Analyst_estimate: { title: "Display Form Feedback", content: "Display real-time quality (e.g., Good/Bad/Incomplete)", state: settingStore.setting.Analyst_estimate },
}))
</script>