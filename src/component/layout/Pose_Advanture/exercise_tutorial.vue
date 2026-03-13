<template>
    <div class="p-3">
        <Trainer :path_json="prop_current_exercise_tutorial" :key="prop_current_exercise_tutorial">{{
            prop_current_exercise_tutorial }}</Trainer>

    </div>
</template>

<script setup>
import Trainer from '../Trainer/Trainer.vue';
defineProps({ prop_current_exercise_tutorial: String })
</script>
