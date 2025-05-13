<template>
    <v-card
        :loading="isLoading"
        :max-width="maxWidth"
        :min-width="minWidth"
        :max-height="maxHeight"
        :width="width"
        height="100%"
        elevation="3"
        class="card-container full-width-card"
    >
        <v-card-title
            v-if="isTitleClickable"
            class="title-wrap mt-2 cursor-pointer"
            @click="$emit('onTitleClick', true)"
        >
            {{ title }}
        </v-card-title>
        <v-card-title v-else class="title-wrap mt-2">
            {{ title }}
        </v-card-title>

        <v-card-subtitle class="subtitle-wrap" v-if="subtitle">
            {{ subtitle }}
        </v-card-subtitle>

        <v-card-text class="pb-0 pt-0">
            <div v-if="isLoading" class="loader-wrap">
                <t-icon name="dashboard-gray" :width="250" :height="250" />
            </div>
            <div v-else class="chart-wrap">
                <slot name="chart"></slot>
            </div>
        </v-card-text>

        <v-card-actions class="justify-space-between">
            <slot name="previous"></slot>
            <div class="text-h7 time-wrap">
                <slot name="interval"></slot>
            </div>
            <slot name="next"></slot>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { TIcon } from '@/components/ui'
defineEmits(['onTitleClick'])

const props = defineProps({
    title: { type: String, required: false, default: 'Область' },
    subtitle: { type: String, required: false },
    width: { type: Number, required: false },
    maxHeight: { type: Number, required: false },
    maxWidth: { type: Number, required: false },
    minWidth: { type: Number, required: false },
    isLoading: { type: Boolean, required: true, default: true },
    isTitleClickable: { type: Boolean, default: false }
})
</script>

<style scoped>
.card-container {
    display: flex;
    flex-direction: column;
    max-height: 90vh;
    overflow: hidden;
}

.full-width-card {
    width: 100% !important; /* Переопределяем ширину */
    max-width: none !important; /* Убираем ограничения max-width */
    min-width: 0 !important; /* Убираем минимальную ширину */
    box-sizing: border-box; /* Учитываем padding и border в ширине */
}

.title-wrap {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 16px;
}

.chart-wrap {
    height: 350;
}
.loader-wrap {
    height: 100%;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}

.subtitle-wrap {
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
    max-width: 100%;
    text-align: left;
    font-size: 14px;
    height: 20px;
}

.time-wrap {
    flex: 1;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
}
</style>
