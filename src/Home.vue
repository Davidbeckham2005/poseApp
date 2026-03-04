<template>
    <div class="flex h-screen bg-[#0a0a0c] text-gray-300 font-sans">
        <Transition enter-active-class="transition-all duration-700 ease-out"
            leave-active-class="transition-all duration-600 ease-in-out" enter-from-class="-translate-x-full opacity-0"
            enter-to-class="translate-x-0 opacity-100" leave-from-class="translate-x-0 opacity-100"
            leave-to-class="-translate-x-full opacity-0">
            <sidebar v-if="!get_state_game" class="w-36 md:w-70 border-r border-gray-800 flex flex-col bg-black"
                :menu-items="menuItems" :current-tab="currentTab" @active-menu="setActive" />
        </Transition>
        <main class="flex-1 flex flex-col overflow-y-auto">
            <Transition enter-active-class="transition-all duration-700 ease-out"
                leave-active-class="transition-all duration-600 ease-in-out"
                enter-from-class="-translate-y-full opacity-0" enter-to-class="translate-y-0 opacity-100"
                leave-from-class="translate-y-0 opacity-100" leave-to-class="-translate-y-full opacity-0">

                <Header v-if="!get_state_game"
                    class="flex items-center justify-between px-6 py-4 border-b border-gray-800"></Header>
            </Transition>
            <div class="py-4 px-2 max-w-6xl mx-auto w-full ">
                <Live v-if="currentTab === `live`"></Live>
                <pose_advanture v-else-if="currentTab == 'game'"></pose_advanture>
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

// console.log(get_state_game())
// component
import Header from './component/layout/Header.vue';
import sidebar from './component/layout/sidebar/sidebar.vue';
import Upload from './component/layout/Upload.vue';
import Settings from './component/layout/Settings.vue';
import History_tab from './component/layout/History/History_tab.vue';
import Live from './component/layout/Live/Live.vue';
import Dashbroad from './component/layout/Dashbroad/dashbroad.vue';
import { useNavigation } from "./composable/helpers";
import Profile from './component/layout/Profile/Profile.vue';
import pose_advanture from './component/layout/Pose_Advanture/pose_advanture.vue';
import { computed, watch } from 'vue';
const { switch_on_sidebar, currentTab } = useNavigation()

const menuItems = [
    { name: 'game', label: 'POSE ADVANTURE', icon: Swords },
    { name: 'live', label: 'LIVE DEMO', icon: Radio },
    { name: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
    { name: 'profile', label: 'Profile', icon: UserRound },
    { name: 'upload', label: 'Upload', icon: UploadIcon },
    { name: 'history', label: 'History', icon: HistoryIcon },
    { name: 'settings', label: 'Settings', icon: SettingsIcon },

];

switch_on_sidebar("game")
// thay doi cac tab
const setActive = (item) => {
    switch_on_sidebar(item.name)
}

</script>