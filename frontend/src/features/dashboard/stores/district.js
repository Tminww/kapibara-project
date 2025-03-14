import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'
import { getLastMonth, getLastQuarter, getLastYear } from '@/utils/utils.js' // Утилиты для дат

export const useDistrictStore = defineStore('district', () => {
	// Состояние
	const loading = ref(false)
	const selectedPeriod = ref('За прошлый месяц')
	const selectedRegions = ref([])
	const startDate = ref('')
	const endDate = ref('')

	const subjects = ref([])
	const statistics = ref({})
	const allStatistics = ref([])
	const selectedDistrictName = ref('')

	const districts = ref([])
	const districtsForRequest = ref([])

	// Геттеры
	const getStartDate = computed(() => startDate.value)
	const getEndDate = computed(() => endDate.value)
	const isLoading = computed(() => loading.value)

	const getSubjects = computed(() => subjects.value)
	const getDistrictName = computed(() => selectedDistrictName.value)
	const getDistrictStat = computed(() => allStatistics.value)
	const getStatistics = computed(() => statistics.value)

	const getAllStatistics = computed(() => allStatistics.value)
	const getRegions = computed(() => statistics.value)
	const getDistrictsForRequest = computed(() => districtsForRequest.value)
	const getDistricts = computed(() => districts.value)

	// Действия
	const dropSubjects = () => {
		subjects.value = []
	}

	const dropDistricts = () => {
		districts.value = []
	}

	const dropDistrictsForRequest = () => {
		districtsForRequest.value = []
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
			selectedDistrictName.value = districtName
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

	// Загрузка субъектов через API
	const loadDistrictsForRequest = async () => {
		try {
			const response = await apiClient.subjects.read()
			districtsForRequest.value = response.map(d => ({
				name: d.name,
				id: d.id,
			}))
			console.log(districtsForRequest.value)
		} catch (error) {
			console.error('Ошибка при загрузке субъектов:', error)
			dropDistrictsForRequest()
		}
	}
	const loadDistricts = async () => {
		try {
			const response = await apiClient.statistics.read()
			districts.value = response.districts
			allStatistics.value = response.stat
			startDate.value = response.startDate // Эти значения могут быть перезаписаны API
			endDate.value = response.endDate
		} catch (error) {
			console.error('Ошибка при загрузке субъектов:', error)
			dropDistricts()
		}
	}

	// Возвращаем все свойства и методы
	return {
		loading,
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
		getRegions,
		getStatistics,
		getSubjects,
		getDistrictsForRequest,
		getDistricts,
		getAllStatistics,

		dropSubjects,
		startLoading,
		endLoading,
		setStatistics,
		dropStatistics,
		loadStatisticsAPI,
		loadSubjectsAPI,
		loadDistrictsForRequest,
		loadDistricts,

		initializeForm,
		updateDatesByPeriod,
		resetForm,
	}
})
