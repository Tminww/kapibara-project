<template>
    <v-form class="form-container" @submit.prevent="$emit('submit', formData)">
        <v-select
            class="mb-3"
            color="primary"
            density="comfortable"
            clearable
            multiple
            hide-details
            variant="outlined"
            :label="district.name"
            item-title="name"
            item-value="id"
            :items="getSubjectItemsAndId(district)"
            :model-value="form.selectedSubjects[district.id] || []"
            @update:modelValue="(value) => (form.selectedSubjects[district.id] = value)"
        >
            <template v-slot:selection="{ item, index }">
                <div v-if="index < 1">
                    <span>{{ item.title }}</span>
                </div>
                <span v-if="index === 1" class="text-caption align-self-center">
                    (+{{ (form.selectedSubjects[district.id] || []).length - 1 }}
                    другие)
                </span>
            </template>
        </v-select>
        <v-divider class="my-4"></v-divider>

        <v-select
            density="comfortable"
            variant="outlined"
            label="Выбрать период"
            v-model="form.selectedPeriod"
            :items="['За прошлый месяц', 'За прошлый квартал', 'За прошлый год']"
            @update:modelValue="updateDatesByPeriod"
        ></v-select>

        <div class="group-date">
            <v-date-input
                label="Дата начала"
                placeholder="DD.MM.YYYY"
                prepend-icon=""
                variant="outlined"
                v-model="form.startDate"
            ></v-date-input>
            <v-date-input
                label="Дата окончания"
                placeholder="DD.MM.YYYY"
                prepend-icon=""
                variant="outlined"
                v-model="form.endDate"
            ></v-date-input>
        </div>

        <div class="group-botton">
            <v-btn
                class="items"
                type="submit"
                :loading="props.loading"
                color="primary"
                variant="tonal"
                text="Применить"
            />
            <v-btn class="items" text="Отменить" color="red" variant="tonal" @click="resetForm" />
        </div>
    </v-form>
</template>

<script setup>
import { onMounted, reactive, watchEffect } from 'vue'
import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils'
import { VDateInput } from 'vuetify/labs/VDateInput'

// Определяем props
const props = defineProps({
    items: { type: Array, required: true },
    loading: { type: Boolean, default: false } // Добавляем prop для состояния загрузки
})

// Определяем emit
const emit = defineEmits(['submit'])

// Локальное реактивное состояние формы
const form = reactive({
    selectedItems: [],
    selectedPeriod: 'За прошлый месяц',
    startDate: null, // Ожидаем строку в формате yyyy-mm-dd или null
    endDate: null // Ожидаем строку в формате yyyy-mm-dd или null
})

// Данные для передачи через emit
const formData = reactive({
    selectedItems: [],
    selectedPeriod: '',
    startDate: null,
    endDate: null
})

// Синхронизация formData с form
watchEffect(() => {
    formData.selectedItems = [...form.selectedItems]
    formData.selectedPeriod = form.selectedPeriod
    formData.startDate = form.startDate
    formData.endDate = form.endDate
})

// Убеждаемся, что хотя бы один регион остаётся выбранным
const ensureAtLeastOneSelected = (newValue) => {
    if (newValue.length === 0) {
        // Если массив пустой, возвращаем последний выбранный регион
        form.selectedItems = [form.selectedItems[0] || props.items[0].id]
    }
}

// Обновление дат по выбранному периоду (локально)
const updateDatesByPeriod = (period) => {
    let interval
    switch (period) {
        case 'За прошлый месяц':
            interval = getLastMonth()
            break
        case 'За прошлый квартал':
            interval = getLastQuarter()
            break
        case 'За прошлый год':
            interval = getLastYear()
            break
        default:
            interval = { startDate: null, endDate: null }
    }
    // Убеждаемся, что даты всегда в формате строки yyyy-mm-dd
    form.startDate = new Date(interval.startDate)
    form.endDate = new Date(interval.endDate)
}

// Сброс формы (локально, с использованием начальных значений из стора)
const resetForm = () => {
    form.selectedItems = props.items.map((s) => s.id) // Все регионы из пропсов
    form.selectedPeriod = 'За прошлый месяц'
    updateDatesByPeriod(form.selectedPeriod)
}

onMounted(() => {
    // Инициализируем локальную форму начальными значениями
    form.selectedItems = props.items.map((s) => s.id)
    form.selectedPeriod = 'За прошлый месяц'
    updateDatesByPeriod(form.selectedPeriod)
})
</script>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
}
.group-botton,
.group-date {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    width: 100%;
    gap: 10px;
}
.items {
    flex: 1;
    min-width: 150px;
}
</style>
