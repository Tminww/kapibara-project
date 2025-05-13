import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'
import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils'

export const useDistrictStore = defineStore('district', () => {
    // Состояние
    const loading = ref(false)
    const selectedPeriod = ref('За прошлый месяц')
    const selectedItems = ref([])
    const startDate = ref('')
    const endDate = ref('')
    const statistics = ref([])
    const allStatistics = ref([])
    const districtsToRequest = ref([])

    // Геттеры
    const getStartDate = computed(() => startDate.value)
    const getEndDate = computed(() => endDate.value)
    const isLoading = computed(() => loading.value)
    const getStatistics = computed(() => statistics.value || [])
    const getAllStatistics = computed(() => allStatistics.value || [])
    const getAllStat = computed(() => allStatistics.value || [])
    const getDistrictsToRequest = computed(() => districtsToRequest.value)
    const getDistrictName = computed(() => allStatistics.value.name || 'Общая статистика')

    // Действия
    const dropDistrictsToRequest = () => {
        districtsToRequest.value = []
    }

    const startLoading = async () => {
        loading.value = true
    }

    const endLoading = async () => {
        loading.value = false
    }

    const setStatistics = (newValue) => {
        statistics.value = Array.isArray(newValue) ? newValue : []
    }

    const dropStatistics = () => {
        statistics.value = []
        allStatistics.value = []
    }

    const initializeForm = () => {
        selectedItems.value = districtsToRequest.value.map((s) => s.id)
        selectedPeriod.value = 'За прошлый месяц'
        updateDatesByPeriod(selectedPeriod.value)
    }

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
        startDate.value = interval.startDate
        endDate.value = interval.endDate
    }

    const resetForm = () => {
        startDate.value = null
        endDate.value = null
        selectedItems.value = districtsToRequest.value.map((s) => s.id)
        selectedPeriod.value = 'За прошлый месяц'
        updateDatesByPeriod(selectedPeriod.value)
    }

    const loadStatistics = async (params) => {
        try {
            const response = await apiClient.statistics.readDistricts(params)
            statistics.value = response.data?.districts || []
            allStatistics.value = response.data?.stat || []

            startDate.value = response.startDate // Эти значения могут быть перезаписаны API
            endDate.value = response.endDate
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropStatistics()
            throw error // Пробрасываем ошибку для обработки в компоненте
        }
    }

    // Загрузка субъектов через API
    const loadDistrictsToRequest = async () => {
        try {
            const response = await apiClient.subjects.readDistricts()
            districtsToRequest.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке субъектов:', error)
            dropDistrictsToRequest()
        }
    }

    return {
        loading,
        districtsToRequest,
        startDate,
        endDate,
        selectedItems,
        selectedPeriod,
        getStartDate,
        getEndDate,
        isLoading,
        getDistrictsToRequest,
        getStatistics,
        getAllStatistics,
        getAllStat,
        getDistrictName,
        startLoading,
        endLoading,
        setStatistics,
        dropStatistics,
        loadDistrictsToRequest,
        loadStatistics,
        initializeForm,
        updateDatesByPeriod,
        resetForm
    }
})
