<template>
    <div class="rounded-2xl bg-gray-700/50 p-5 mt-5 space-y-5 border border-white/20 text-white">
        <h1 class="font-semibold text-white text-xl">Account Settings</h1>
        <div class="flex flex-col">
            <span class="text-gray-500 text-lg">Full name</span>
            <input type="text" class="border bg-gray-800/90 h-10 pl-5 rounded-xl mt-2" v-model="name">
        </div>
        <div class="flex flex-col">
            <span class="text-gray-500 text-lg">Email</span>
            <input type="text" class="border bg-gray-800/90 h-10 pl-5 rounded-xl mt-2" v-model="email">
        </div>
        <Profile_btn @click="update_user_handle" text="Save Changes"></Profile_btn>
    </div>
</template>

<script setup>
import { useUser } from '../../../store/user.store';
import { update_user } from '../../../services/app.service';
const props = defineProps({ user: Object })
const userStore = useUser()
import Profile_btn from './Profile_btn.vue';
import { ref } from 'vue'
const name = ref(props.user.name)
const email = ref(props.user.email)
console.log(name.value, email.value)
const update_user_handle = async () => {
    if (name == props.user.name && props.email.user.email) return
    const data = {
        "name": name.value,
        "email": email.value,
    }
    const res = await update_user(data)
    await userStore.fetchUser()
}
</script>
