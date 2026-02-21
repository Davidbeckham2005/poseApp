<script setup>
import {
    SunIcon,
    Bell,
    User,
} from 'lucide-vue-next';
import cp_button from '../bases/cp_button.vue';
import title_content from '../bases/title_content.vue';
</script>
<template>
    <header>
        <title_content title="Pose Detection Studio" content="Real - time exercise analysis"></title_content>
        <div class="flex items-center space-x-3">
            <cp_button :icon="Bell"></cp_button>
            <cp_button :icon="SunIcon"></cp_button>
            <cp_button :icon="User" class="text-cyan-500/70"></cp_button>
        </div>
    </header>
</template>