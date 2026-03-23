<template>
    <div @click.once="unclock" class="flex h-screen dark:bg-[#0a0a0c] dark:text-gray-300 font-sans">
        <sidebar v-if="!get_state_game" class="w-36 md:w-70 border-r border-gray-800 flex flex-col dark:bg-black"
            :menu-items="menuItems" :current-tab="currentTab" @active-menu="setActive" />
        <main class="flex-1 flex flex-col overflow-y-auto">
            <Header v-if="!get_state_game" class="flex justify-end px-6 py-4 border-b border-gray-800">
            </Header>
            <div class="py-4 px-2 max-w-6xl mx-auto w-full ">
                <UserDashboard v-if="currentTab === `home`"></UserDashboard>
                <pose_advanture v-else-if="currentTab == 'game'"></pose_advanture>
                <Profile v-else-if="currentTab === `profile`"></Profile>
                <MealPlanner v-else-if="currentTab === `meals`"></MealPlanner>
                <CameraView v-else-if="currentTab === 'test'"></CameraView>
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
    HistoryIcon,
    SettingsIcon,
    UploadIcon,
    UserRound,
    Swords,
    Home,
    Apple,
} from 'lucide-vue-next';
// game
import { state_game } from './composable/help_game';
const { get_state_game } = state_game()
const unclock = () => {
    unlockAudio()
}
// console.log(get_state_game())
// component
import CameraView from './component/layout/Pose_Advanture/CameraView.vue';
import Header from './component/layout/Header.vue';
import sidebar from './component/layout/sidebar/sidebar.vue';
import Upload from './component/layout/Upload.vue';
import Settings from './component/layout/Settings.vue';
import History_tab from './component/layout/History/History_tab.vue';
import Dashbroad from './component/layout/Dashbroad/dashbroad.vue';
import { useNavigation } from "./composable/helpers";
import Profile from './component/layout/Profile/Profile.vue';
import pose_advanture from './component/layout/Pose_Advanture/pose_advanture.vue';
import UserDashboard from './component/layout/UserDashboard.vue';
import MealPlanner from './component/layout/MealPlanner.vue';
import { useAudio } from './composable/audio';
const { unlockAudio, speak } = useAudio()
const { switch_on_sidebar, currentTab } = useNavigation()

const menuItems = [
    { name: 'game', label: 'FITNESS ADVENTURE', icon: Swords },
    { name: 'profile', label: 'Trang cá nhân', icon: UserRound },
    { name: 'meals', label: 'Bữa ăn & Dinh dưỡng', icon: Apple },
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