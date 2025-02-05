import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'

export const useStatisticStore = defineStore('statistic', () => {
	const statistics = ref({})

	// Геттер для получения регионов в определенном округе
	const getRegionsInDistrict = computed(districtId => {
		return statistics.value.districts[districtId]
	})

	// Геттер для получения всей статистики
	const getAllStatistics = computed(() => {
		return {
			name: statistics.value.name,
			count: statistics.value.count,
			stat: statistics.value.stat,
		}
	})

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
	const loadStatisticsAPI = async () => {
		statistics.value = await apiClient.statistics.readOneRegion(12)
	}

	// Обновление статистики через API
	const updateStatisticsAPI = async parameters => {
		statistics.value = await apiClient.statistics.read(parameters)
	}
	return {
		statistics,
		getRegionsInDistrict,
		getAllStatistics,
		getStatistics,
		setStatistics,
		dropStatistics,
		loadStatisticsAPI,
		updateStatisticsAPI,
	}
})
