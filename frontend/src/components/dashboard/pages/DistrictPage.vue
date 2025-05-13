<template>
    <t-filter-sidebar v-model="leftMenu" :loading="loadingSubjects">
        <template #form>
            <t-filter-form
                :loading="store.isLoading"
                :items="store.getDistrictsToRequest"
                @submit="(data) => onSubmit(data)"
            ></t-filter-form>
        </template>
    </t-filter-sidebar>

    <v-row no-gutters class="justify-start">
        <v-col>
            <v-container fluid class="my-0 py-0">
                <v-btn color="primary" variant="tonal" @click="leftMenu = !leftMenu">
                    Фильтры
                </v-btn>
            </v-container>
        </v-col>
    </v-row>

    <v-row v-if="errorStatistics || errorSubjects">
        <v-col>
            <v-container fluid>
                <v-alert
                    v-if="errorSubjects"
                    class="d-flex align-center justify-center"
                    type="error"
                    title="Произошла ошибка"
                    :text="errorStatistics || errorSubjects"
                    variant="tonal"
                ></v-alert>
            </v-container>
        </v-col>
    </v-row>

    <v-row v-else no-gutters class="justify-space-around">
        <v-col cols="auto" v-if="store.getAllStat?.length">
            <v-container>
                <t-region-card
                    :title="store.getDistrictName || 'Общая статистика'"
                    :is-loading="isLoading"
                    :min-width="400"
                    :max-width="400"
                >
                    <template #chart>
                        <t-donut-chart
                            :labels="store.getAllStat.map((item) => item.name)"
                            :series="store.getAllStat.map((item) => item.count)"
                            :height="350"
                            :enable-logarithmic="false"
                            :log-base="10"
                            :y-start-value="0"
                            legend-position="bottom"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isPreviousLoading"
                            @click="previousInterval"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next>
                        <v-btn color="primary" :loading="isNextLoading" @click="nextInterval">
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isLoading">
                        {{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }} -
                        {{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
                    </template>
                </t-region-card>
            </v-container>
        </v-col>

        <v-col cols="auto" v-for="region in store.getStatistics" :key="region.name">
            <v-container v-if="region?.stat?.length">
                <t-region-card
                    :title="region.name || 'Без названия'"
                    :is-loading="isLoading"
                    :min-width="400"
                    :max-width="400"
                >
                    <template #chart>
                        <t-donut-chart
                            :labels="region.stat.map((item) => item.name)"
                            :series="region.stat.map((item) => item.count)"
                            :height="350"
                            :enable-logarithmic="false"
                            :log-base="10"
                            :y-start-value="0"
                            legend-position="bottom"
                        />
                    </template>
                    <template #previous>
                        <v-btn
                            color="primary"
                            :loading="isPreviousLoading"
                            @click="previousInterval"
                        >
                            <v-icon>mdi-arrow-left</v-icon>
                        </v-btn>
                    </template>
                    <template #next>
                        <v-btn color="primary" :loading="isNextLoading" @click="nextInterval">
                            <v-icon>mdi-arrow-right</v-icon>
                        </v-btn>
                    </template>
                    <template #interval v-if="!isLoading">
                        {{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }} -
                        {{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
                    </template>
                </t-region-card>
            </v-container>
        </v-col>
    </v-row>
</template>

<script setup>
import { TRegionCard, TDonutChart, TFilterSidebar, TFilterForm } from '../widgets'
import { useDistrictStore } from '../stores/district'
import { dateFormat, getLastMonth } from '@/utils/utils'
import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

const store = useDistrictStore()

const leftMenu = ref(false)
const isPreviousLoading = ref(false)
const isNextLoading = ref(false)
const loadingSubjects = ref(false)
const errorSubjects = ref(null)
const loadingStatistics = ref(false)
const errorStatistics = ref(null)

const isLoading = computed(() => store.isLoading || loadingStatistics.value)

const getParams = () => {
    const params = {
        startDate: store.startDate,
        endDate: store.endDate
    }
    if (store.selectedItems.length > 0) {
        params.ids = store.selectedItems.toString()
    }
    return params
}

// Переход к предыдущему интервалу
const previousInterval = async () => {
    try {
        isPreviousLoading.value = true
        loadingStatistics.value = true
        errorStatistics.value = null

        // Сдвигаем дату на месяц назад относительно текущего startDate
        const currentStart = new Date(store.startDate)

        const newInterval = getLastMonth(currentStart)
        store.startDate = newInterval.startDate
        store.endDate = newInterval.endDate

        const params = getParams()
        await store.loadStatistics(params)
    } catch (e) {
        errorStatistics.value = e.message
        store.dropStatistics()
    } finally {
        isPreviousLoading.value = false
        loadingStatistics.value = false
    }
}

// Переход к следующему интервалу
const nextInterval = async () => {
    try {
        // Сдвигаем дату на месяц вперёд относительно текущего endDate
        const currentStart = new Date(store.startDate)
        currentStart.setMonth(currentStart.getMonth() + 1)

        if (currentStart > new Date()) {
            toast.warning('Нельзя переходить в будущее')
            return
        }

        currentStart.setMonth(currentStart.getMonth() + 1)

        isNextLoading.value = true
        loadingStatistics.value = true
        errorStatistics.value = null

        const newInterval = getLastMonth(currentStart)
        store.startDate = newInterval.startDate
        store.endDate = newInterval.endDate

        const params = getParams()
        await store.loadStatistics(params)
    } catch (e) {
        errorStatistics.value = e.message
        store.dropStatistics()
    } finally {
        isNextLoading.value = false
        loadingStatistics.value = false
    }
}

const convertDateToYYYYMMDDString = (date) => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}

const paramsProcessing = (selected, startDate, endDate) => {
    const params = {}
    if (startDate) params.startDate = startDate
    if (endDate) params.endDate = endDate
    if (selected.length > 0) params.ids = selected.toString()
    return params
}

const onSubmit = async (data) => {
    try {
        await store.startLoading()
        store.selectedItems = [...data.selectedItems]
        store.selectedPeriod = data.selectedPeriod
        store.startDate = convertDateToYYYYMMDDString(data.startDate)
        store.endDate = convertDateToYYYYMMDDString(data.endDate)

        const params = paramsProcessing(store.selectedItems, store.startDate, store.endDate)
        await store.loadStatistics(params)
    } catch (e) {
        store.dropStatistics()
    } finally {
        await store.endLoading()
    }
}

const loadInitialData = async () => {
    try {
        loadingSubjects.value = true
        errorSubjects.value = null
        await store.loadDistrictsToRequest()

        loadingStatistics.value = true
        errorStatistics.value = null
        store.initializeForm()
        const params = getParams()
        await store.loadStatistics(params)
    } catch (e) {
        errorSubjects.value = e.message
        errorStatistics.value = e.message
        store.dropStatistics()
    } finally {
        loadingSubjects.value = false
        loadingStatistics.value = false
    }
}

onMounted(async () => {
    await loadInitialData()
})
</script>

<style scoped></style>
