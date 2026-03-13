<script setup>
import { computed, ref } from 'vue';
import { Camera, Mail, Calendar, Edit3, LayoutDashboard, Settings } from 'lucide-vue-next'
import { useUser } from '../../../store/user.store';
import { open } from "@tauri-apps/plugin-dialog";
import { convertFileSrc } from "@tauri-apps/api/core";

// Components
import Profile_overview from './Profile_overview.vue';
import Profile_setting from './Profile_setting.vue';
import Profile_btn from './Profile_btn.vue';
import Show_profile_value from './show_profile_value.vue';


const userStore = useUser();
const avatar = ref(userStore.user.avatar || "https://via.placeholder.com/150");

const stats = computed(() => [
    { label: 'Số phiên tập', value: userStore.user.total_session + " phiên", icon: 'activity', color: 'text-orange-400' },
    { label: 'Thời gian', value: userStore.user.total_time_work + " phút", icon: 'clock', color: 'text-purple-400' },
    { label: 'Tổng calo', value: userStore.user.total_caloris + " calo", icon: 'zap', color: 'text-amber-400' },
    { label: 'Trung bình chính xác', value: userStore.user.avg_accuracy + "%", icon: 'target', color: 'text-emerald-400' },
]);

async function change_avatar() {
    try {
        const pathSelected = await open({
            multiple: false,
            filters: [{ name: "Images", extensions: ["png", "jpg", "jpeg", "webp"] }]
        });
        if (pathSelected) avatar.value = convertFileSrc(pathSelected);
    } catch (error) {
        console.error("Avatar upload error:", error);
    }
}

const current_tab = ref('Overview');
const tabs = [
    { id: 'Overview', name: 'Tổng quan', icon: LayoutDashboard },
    { id: 'Setting', name: 'Cài đặt', icon: Settings }
];
</script>

<template>
    <div class="max-w-6xl mx-auto p-6 space-y-8">
        <div
            class="relative overflow-hidden bg-white dark:bg-gray-800/40 backdrop-blur-md border border-gray-200 dark:border-gray-700 rounded-3xl p-8 shadow-xl">
            <div class="absolute top-0 right-0 -mt-4 -mr-4 w-32 h-32 bg-orange-500/10 rounded-full blur-3xl"></div>
            <div class="flex flex-col md:flex-row items-center gap-8 relative z-10">
                <div class="relative group cursor-pointer" @click="change_avatar">
                    <div
                        class="w-32 h-32 rounded-2xl overflow-hidden border-4 border-white dark:border-gray-700 shadow-2xl transition-transform duration-300 group-hover:scale-105">
                        <img :src="avatar" alt="Profile" class="w-full h-full object-cover" />
                    </div>
                    <div
                        class="absolute -bottom-2 -right-2 bg-orange-500 p-2.5 rounded-xl shadow-lg text-white transform transition-all duration-300 hover:scale-110">
                        <Camera :size="20" />
                    </div>
                    <div
                        class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl">
                        <span class="text-white text-xs font-medium">Thay đổi ảnh</span>
                    </div>
                </div>
                <div class="flex-1 text-center md:text-left space-y-3">
                    <div>
                        <h1 class="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">
                            {{ userStore.user.name }}
                        </h1>
                        <div
                            class="flex flex-wrap justify-center md:justify-start gap-4 mt-2 text-gray-500 dark:text-gray-400">
                            <span class="flex items-center gap-1.5 text-sm">
                                <Mail :size="16" class="text-orange-400" /> {{ userStore.user.email }}
                            </span>
                            <span
                                class="flex items-center gap-1.5 text-sm border-l border-gray-300 dark:border-gray-600 pl-4">
                                <Calendar :size="16" class="text-orange-400" /> Tham gia: {{ userStore.user.joined }}
                            </span>
                        </div>
                    </div>

                    <div class="pt-2">
                        <button @click="current_tab = 'Setting'"
                            class="inline-flex items-center gap-2 px-6 py-2.5 bg-gray-900 dark:bg-white dark:text-gray-900 text-white rounded-xl font-semibold text-sm hover:bg-orange-500 dark:hover:bg-orange-400 transition-all shadow-md active:scale-95">
                            <Edit3 :size="16" /> Thiết lập tài khoản
                        </button>
                    </div>
                    <div>

                    </div>
                </div>
            </div>
        </div>

        <div class="space-y-6">
            <div class="flex border-b border-gray-200 dark:border-gray-700 overflow-x-auto">
                <button v-for="tab in tabs" :key="tab.id" @click="current_tab = tab.id" :class="[
                    'flex items-center gap-2 px-8 py-4 text-sm font-bold uppercase tracking-wider transition-all relative',
                    current_tab === tab.id
                        ? 'text-orange-500'
                        : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                ]">
                    <component :is="tab.icon" :size="18" />
                    {{ tab.name }}
                    <div v-if="current_tab === tab.id"
                        class="absolute bottom-0 left-0 right-0 h-1 bg-orange-500 rounded-t-full"></div>
                </button>
            </div>

            <Transition mode="out-in" enter-active-class="transition duration-200 ease-out"
                enter-from-class="opacity-0 translate-y-4" enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-4">
                <div :key="current_tab" class="min-h-[400px]">
                    <Profile_overview v-if="current_tab === 'Overview'" :stats="stats" />
                    <Profile_setting v-else-if="current_tab === 'Setting'" :user="userStore.user" />
                </div>
            </Transition>
        </div>
    </div>
</template>

<style scoped>
.overflow-x-auto::-webkit-scrollbar {
    display: none;
}

.overflow-x-auto {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>