<template>
    <v-app style="background: none">
        <main-layout>
            <router-view> </router-view>
        </main-layout>
    </v-app>
</template>

<script setup lang="ts">
import { default as MainLayout } from '@/layouts/MainLayout.vue'
</script>

<style scoped></style>
