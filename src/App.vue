<script setup>
import Home from './Home.vue';
import Trainer from './component/Trainer/Trainer.vue';
import { useUser } from './store/user.store';
import { useVideo } from './store/video.store';
import { useSetting } from './store/setting.store';
import { onMounted } from 'vue';
const userStore = useUser()
const videoStore = useVideo()
const settingStore = useSetting()
onMounted(async () => {
  await userStore.fetchUser()
  await videoStore.fetchVideo()

})
</script>

<template>
  <router-view>
    <Home v-if="userStore.user"></Home>
    <!-- <Trainer></Trainer> -->
  </router-view>
</template>
