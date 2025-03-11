import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'
import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils.js' // Утилиты для дат

export const useDistrictStore = defineStore('district', () => {
	// Состояние
	const loading = ref(false)
	const name = ref('')
	const statistics = ref({})
	const allStatistics = ref([])
	const subjects = ref([])
	const startDate = ref('')
	const endDate = ref('')
	const selectedRegions = ref([])
	const selectedPeriod = ref('За прошлый месяц') // Добавляем selectedPeriod

	// Геттеры
	const getStartDate = computed(() => startDate.value)
	const getEndDate = computed(() => endDate.value)
	const getDistrictName = computed(() => name.value)
	const getDistrictStat = computed(() => allStatistics.value)
	const isLoading = computed(() => loading.value)
	const getDistrict = computed(() => allStatistics.value)
	const getRegions = computed(() => statistics.value)
	const getStatistics = computed(() => statistics.value)
	const getSubjects = computed(() => subjects.value)

	// Действия
	const dropSubjects = () => {
		subjects.value = []
	}

	const startLoading = async () => {
		loading.value = true
	}

	const endLoading = async () => {
		loading.value = false
	}

	const setStatistics = newValue => {
		statistics.value = newValue
	}

	const dropStatistics = () => {
		statistics.value = {}
	}

	// Инициализация данных формы
	const initializeForm = () => {
		selectedRegions.value = subjects.value.map(s => s.id)
		selectedPeriod.value = 'За прошлый месяц'
		updateDatesByPeriod(selectedPeriod.value)
	}

	// Обновление дат по выбранному периоду
	const updateDatesByPeriod = period => {
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

	// Сброс формы
	const resetForm = () => {
		startDate.value = null
		endDate.value = null
		selectedRegions.value = subjects.value.map(s => s.id)
		selectedPeriod.value = 'За прошлый месяц'
		updateDatesByPeriod(selectedPeriod.value)
	}

	// Загрузка статистики через API
	const loadStatisticsAPI = async (districtName, parameters) => {
		try {
			const response = await apiClient.statistics.read(parameters)
			name.value = response.districts.filter(
				d => d.name === districtName,
			)[0].name
			statistics.value = response.districts.filter(
				d => d.name === districtName,
			)[0].regions
			allStatistics.value = response.stat
			startDate.value = response.startDate // Эти значения могут быть перезаписаны API
			endDate.value = response.endDate
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropStatistics()
			throw error // Пробрасываем ошибку для обработки в компоненте
		}
	}

	// Загрузка субъектов через API
	const loadSubjectsAPI = async districtName => {
		try {
			const response = await apiClient.subjects.read()
			subjects.value = response.filter(
				d => d.name === districtName,
			)[0].regions
		} catch (error) {
			console.error('Ошибка при загрузке субъектов:', error)
			dropSubjects()
		}
	}

	// Возвращаем все свойства и методы
	return {
		loading,
		name,
		statistics,
		allStatistics,
		subjects,
		startDate,
		endDate,
		selectedRegions,
		selectedPeriod,

		getStartDate,
		getEndDate,
		getDistrictName,
		getDistrictStat,
		isLoading,
		getDistrict,
		getRegions,
		getStatistics,
		getSubjects,

		dropSubjects,
		startLoading,
		endLoading,
		setStatistics,
		dropStatistics,
		loadStatisticsAPI,
		loadSubjectsAPI,

		initializeForm,
		updateDatesByPeriod,
		resetForm,
	}
})
