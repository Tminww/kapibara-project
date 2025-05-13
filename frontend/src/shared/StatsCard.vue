<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{
    color: 'success' | 'error' | 'warning' | 'info' | 'primary'
    icon: 'check' | 'alert' | 'info' | 'help' | 'clock'
    amount: string | number
    description: string
}>()

const mapIconToMdi = {
    check: 'mdi-check-circle',
    alert: 'mdi-alert-circle',
    info: 'mdi-information',
    help: 'mdi-help-circle',
    clock: 'mdi-clock-outline'
}

const currentIcon = computed(() => {
    return mapIconToMdi[props.icon]
})
</script>

<template>
    <v-card class="h-100" elevation="3">
        <v-card-text class="text-center">
            <v-avatar :color="color" size="60" class="mb-4" variant="tonal">
                <v-icon size="32" :icon="currentIcon"></v-icon>
            </v-avatar>
            <h2 class="mb-2">{{ amount }}</h2>
            <p>{{ description }}</p>
        </v-card-text>
    </v-card>
</template>
