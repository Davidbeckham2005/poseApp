<script setup>
// import Home from './Home.vue';
// import Trainer from './component/Trainer/Trainer.vue';
import { useUser } from './store/user.store';
import { useVideo } from './store/video.store';
import { useSetting } from './store/setting.store';
import { onMounted } from 'vue';
import { useWellness } from './store/wellness.store';

const userStore = useUser()
const videoStore = useVideo()
const settingStore = useSetting()
const wellnessStore = useWellness()


onMounted(async () => {
  await userStore.fetchUser()
  await videoStore.fetchVideo()
  await wellnessStore.fetchDailyNutrition(userStore.user?.id, ('2026-03-23'))
  // await wellnessStore.fetchDailyNutrition(userStore.user?.id, new Date().toISOString().split('T')[0])
  await wellnessStore.get_all_food_items()
})
</script>

<template>
  <router-view />
  <!-- <Home v-if="userStore.user"></Home> -->
  <!-- <Trainer></Trainer> -->
  <!-- </router-view> -->
</template>
