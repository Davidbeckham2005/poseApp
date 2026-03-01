<template>
    <div class="flex h-screen bg-[#0a0a0c] text-gray-300 font-sans">
        <sidebar class="w-36 md:w-70 border-r border-gray-800 flex flex-col" :menu-items="menuItems"
            :current-tab="currentTab" @active-menu="setActive">
        </sidebar>
        <main class="flex-1 flex flex-col overflow-y-auto">
            <Header class="flex items-center justify-between px-6 py-4 border-b border-gray-800"></Header>
            <div class="py-4 px-4 max-w-6xl mx-auto w-full ">
                <Live v-if="currentTab === `live`"></Live>
                <Dashbroad v-else-if="currentTab === `dashboard`"></Dashbroad>
                <Upload v-else-if="currentTab === `upload`"></Upload>
                <Settings v-else-if="currentTab === `settings`"></Settings>
                <History_tab v-else-if="currentTab === `history`"></History_tab>
            </div>
        </main>
    </div>
</template>

<script setup>
import {
    LayoutDashboardIcon as DashboardIcon,
    HistoryIcon,
    SettingsIcon,
    UploadIcon,
    Radio,

} from 'lucide-vue-next';
// component
import Header from './component/layout/Header.vue';
import sidebar from './component/layout/sidebar/sidebar.vue';
import Upload from './component/layout/Upload.vue';
import Settings from './component/layout/Settings.vue';
import History_tab from './component/layout/History/History_tab.vue';
import Live from './component/layout/Live/Live.vue';
import Dashbroad from './component/layout/Dashbroad/dashbroad.vue';
import { useNavigation } from "./composable/helpers";
const { switch_on_sidebar, currentTab } = useNavigation()

const menuItems = [
    { name: 'live', label: 'LIVE DEMO', icon: Radio },
    { name: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
    { name: 'upload', label: 'Upload', icon: UploadIcon },
    // { name: 'analysis', label: 'Analysis', icon: AnalysisIcon },
    { name: 'history', label: 'History', icon: HistoryIcon },
    { name: 'settings', label: 'Settings', icon: SettingsIcon },

];
switch_on_sidebar("upload")
// thay doi cac tab
const setActive = (item) => {
    switch_on_sidebar(item.name)
}
</script>