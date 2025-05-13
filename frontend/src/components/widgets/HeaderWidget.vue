<template>
    <v-app-bar :color="color">
        <template #title>
            <div class="cursor-pointer">
                <slot name="title"></slot>
            </div>
        </template>

        <template #append>
            <div class="cursor-pointer pr-10">
                <slot name="auth"></slot>
            </div>
        </template>
    </v-app-bar>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
const { color = 'primary' } = defineProps<{
    color?: string
}>()
</script>
