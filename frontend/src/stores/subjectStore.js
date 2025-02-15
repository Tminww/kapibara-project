import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'

export const useSubjectStore = defineStore('subject', () => {
	const loading = ref(false)

	const statistics = ref({})
	const subjects = ref([])

	const getRegionsToRequest = computed(() => {
		return subjects.value
	})

	const dropRegionsToRequest = () => {
		subjects.value = []
	}

	const loadSubjectsAPI = async () => {
		const response = await apiClient.subjects.read()
		subjects.value = response
	}
	// Геттер для получения регионов в определенном округе
	const getRegionsInDistrict = computed(districtId => {
		return statistics.value.districts[districtId]
	})

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
	const getDistricts = computed(() => {
		return statistics.value.districts
	})

	// Геттер для получения всей статистики
	const getStatistics = computed(() => {
		return statistics.value
	})

	// Установка статистики
	const setStatistics = newValue => {
		statistics.value = newValue
	}

	// Сброс статистики
	const dropStatistics = () => {
		statistics.value = {}
	}

	// Загрузка статистики с API

	// Обновление статистики через API
	const loadSubjectStatisticsAPI = async parameters => {
		statistics.value = await apiClient.statistics.read(parameters)
	}
	// Обновление статистики через API

	return {
		statistics,
		getRegionsInDistrict,

		getStatistics,
		getDistricts,

		setStatistics,
		dropStatistics,
		loadSubjectStatisticsAPI,

		isLoading,
		startLoading,
		endLoading,

		getRegionsToRequest,
		dropRegionsToRequest,
		loadSubjectsAPI,
	}
})
