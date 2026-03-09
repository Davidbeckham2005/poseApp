<template>
    <div @click.once="unclock" class="flex h-screen bg-[#0a0a0c] text-gray-300 font-sans">

        <sidebar v-if="!get_state_game" class="w-36 md:w-70 border-r border-gray-800 flex flex-col bg-black"
            :menu-items="menuItems" :current-tab="currentTab" @active-menu="setActive" />

        <main class="flex-1 flex flex-col overflow-y-auto">


            <Header v-if="!get_state_game" class="flex items-center justify-between px-6 py-4 border-b border-gray-800">
            </Header>

            <div class="py-4 px-2 max-w-6xl mx-auto w-full ">
                <!-- <Live v-if="currentTab === `live`"></Live> -->
                <pose_advanture v-if="currentTab == 'game'"></pose_advanture>
                <Profile v-if="currentTab === `profile`"></Profile>
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
    UserRound,
    Swords,
} from 'lucide-vue-next';
// game
import { state_game } from './composable/help_game';
const { get_state_game } = state_game()
const unclock = () => {
    unlockAudio()
}
// console.log(get_state_game())
// component
import Header from './component/layout/Header.vue';
import sidebar from './component/layout/sidebar/sidebar.vue';
import Upload from './component/layout/Upload.vue';
import Settings from './component/layout/Settings.vue';
import History_tab from './component/layout/History/History_tab.vue';
import Dashbroad from './component/layout/Dashbroad/dashbroad.vue';
import { useNavigation } from "./composable/helpers";
import Profile from './component/layout/Profile/Profile.vue';
import pose_advanture from './component/layout/Pose_Advanture/pose_advanture.vue';
// import lobby from './component/layout/Pose_Advanture/Warmup.vue'
import { useAudio } from './composable/audio';
const { unlockAudio, speak } = useAudio()
const { switch_on_sidebar, currentTab } = useNavigation()

const menuItems = [
    { name: 'game', label: 'FITNESS ADVENTURE', icon: Swords },
    // { name: 'live', label: 'LIVE DEMO', icon: Radio },
    // { name: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
    { name: 'profile', label: 'Trang cá nhân', icon: UserRound },
    { name: 'upload', label: 'Kiểm tra tập luyện', icon: UploadIcon },
    { name: 'history', label: 'lịch sử', icon: HistoryIcon },
    { name: 'settings', label: 'Cài đặt', icon: SettingsIcon },

];

switch_on_sidebar("game")
// thay doi cac tab
const setActive = (item) => {
    switch_on_sidebar(item.name)
}

</script>