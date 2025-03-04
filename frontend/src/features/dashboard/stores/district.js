import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'

export const useDistrictStore = defineStore('district', () => {
	const loading = ref(false)

	const name = ref('')
	const statistics = ref({})
	const allStatistics = ref([])
	const subjects = ref([])
	const startDate = ref('')
	const endDate = ref('')

	const getStartDate = computed(() => {
		return startDate.value
	})

	const getEndDate = computed(() => {
		return endDate.value
	})

	const getDistrictName = computed(() => {
		return name.value
	})

	const getDistrictStat = computed(() => {
		return allStatistics.value
	})
	const dropSubjects = () => {
		subjects.value = []
	}

	const isLoading = computed(() => {
		return loading.value
	})

	const startLoading = async () => {
		loading.value = true
	}

	const endLoading = async () => {
		loading.value = false
	}

	// Геттер для получения всех округов
	const getDistrict = computed(() => {
		return allStatistics.value
	})
	// Геттер для получения всех округов
	const getRegions = computed(() => {
		return statistics.value
	})

	// Геттер для получения всей статистики
	const getStatistics = computed(() => {
		return statistics.value
	})

	// Геттер для получения всей статистики
	const getSubjects = computed(() => {
		return subjects.value
	})

	// Установка статистики
	const setStatistics = newValue => {
		statistics.value = newValue
	}

	// Сброс статистики
	const dropStatistics = () => {
		statistics.value = {}
	}

	const loadStatisticsAPI = async (districtName, parameters) => {
		const response = await apiClient.statistics.read(parameters)
		name.value = response.districts.filter(
			d => d.name === districtName,
		)[0].name

		statistics.value = response.districts.filter(
			d => d.name === districtName,
		)[0].regions

		allStatistics.value = response.stat

		startDate.value = response.startDate
		endDate.value = response.endDate
	}

	const loadSubjectsAPI = async districtName => {
		try {
			let response = await apiClient.subjects.read()

			subjects.value = response.filter(
				d => d.name === districtName,
			)[0].regions
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropSubjects()
		}
	}
	// Обновление статистики через API

	return {
		statistics,

		getStatistics,
		getDistrict,
		getRegions,
		getDistrictName,

		setStatistics,
		dropStatistics,
		loadStatisticsAPI,

		isLoading,
		startLoading,
		endLoading,

		getSubjects,
		dropSubjects,
		loadSubjectsAPI,

		getStartDate,
		getEndDate,

		getDistrictStat,
	}
})
