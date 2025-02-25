import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'
import { allDocumentTypes, allOrgans } from '@/mock'

export const useDashboardStore = defineStore('dashboard', () => {
	const emptyResponse = {
		name: '',
		count: 0,
		stat: [], // Пустой массив по умолчанию
		startDate: null,
		endDate: null,
	}
	const publicationByYears = ref({ ...emptyResponse })
	const secondAreaStatistics = ref([])
	const publicationByNomenclature = ref({ ...emptyResponse })
	const fifthAreaStatistics = ref([])
	const sixthAreaStatistics = ref([])

	const thirdAreaStatistics = ref({})

	// Геттер для получения регионов в определенном округе
	const getRegionsInDistrict = computed(districtId => {
		return thirdAreaStatistics.value.districts[districtId]
	})

	// Геттер для получения всей статистики
	const getAllStatistics = computed(() => {
		return {
			name: thirdAreaStatistics.value.name,
			count: thirdAreaStatistics.value.count,
			stat: thirdAreaStatistics.value.stat,
		}
	})

	const getPublicationByYears = computed(() => {
		return publicationByYears.value.stat
	})

	const getPublicationByYearsSeries = computed(() => {
		return publicationByYears.value?.stat?.map(row => row.count)
	})

	const getPublicationByYearsLabels = computed(() => {
		return publicationByYears.value?.stat?.map(row => row.name)
	})
	const getSecondAreaDocumentsStatisticsByMonth = computed(() => {
		return secondAreaStatistics.value
	})
	const getPublicationByNomenclature = computed(() => {
		return publicationByNomenclature.value.stat
	})

	const getPublicationByNomenclatureSeries = computed(() => {
		return publicationByNomenclature.value?.stat?.map(row => row.count)
	})

	const getPublicationByNomenclatureLabels = computed(() => {
		return publicationByNomenclature.value?.stat?.map(row => row.name)
	})

	const getFifthAreaDocumentsStatisticsByQuarter = computed(() => {
		return fifthAreaStatistics.value
	})
	const getSixthAreaDocumentsStatisticsByQuarter = computed(() => {
		return sixthAreaStatistics.value
	})

	// Геттер для получения всех округов
	const getDistricts = computed(() => {
		return thirdAreaStatistics.value.districts
	})

	// Геттер для получения всей статистики
	const getStatistics = computed(() => {
		return thirdAreaStatistics.value
	})

	// Установка статистики
	const setStatistics = newValue => {
		thirdAreaStatistics.value = newValue
	}

	// Сброс статистики
	const dropStatistics = () => {
		thirdAreaStatistics.value = {}
	}
	const dropPublicationByYears = () => {
		publicationByYears.value = { ...emptyResponse }
	}
	const dropSecondAreaDocumentsStatisticsByMonth = () => {
		secondAreaStatistics.value = []
	}
	const dropPublicationByNomenclature = () => {
		publicationByNomenclature.value = { ...emptyResponse }
	}
	const dropFifthAreaDocumentsStatisticsByQuarter = () => {
		fifthAreaStatistics.value = []
	}
	const dropSixthAreaDocumentsStatisticsByQuarter = () => {
		sixthAreaStatistics.value = []
	}

	// Загрузка статистики с API
	const loadStatisticsAPI = async () => {
		thirdAreaStatistics.value = await apiClient.statistics.readOneRegion(12)
	}

	// Обновление статистики через API
	const updateStatisticsAPI = async parameters => {
		thirdAreaStatistics.value = await apiClient.statistics.read(parameters)
	}
	// Обновление статистики через API
	const loadPublicationByYears = async parameters => {
		try {
			let response = await apiClient.publicationByYears.read(parameters)

			publicationByYears.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByYears()
		}
	}
	const loadSecondAreaDocumentsStatisticsByMonth = async parameters => {
		try {
			let allData = await apiClient.statistics.read(parameters)
			console.log(
				'loadSecondAreaDocumentsStatisticsByMonth',
				allData.stat,
			)

			allData = allData.stat || [] // Проверяем, что `stat` существует

			let newData = [...allData] // Копируем данные вместо `join`

			// Проверяем и добавляем отсутствующие объекты
			// allDocumentTypes.forEach(docType => {
			// 	const exists = newData.some(data => data.name === docType.name)
			// 	if (!exists) {
			// 		newData.push({ name: docType.name, count: 0 })
			// 	}
			// })

			secondAreaStatistics.value = newData
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropSecondAreaDocumentsStatisticsByMonth()
		}
	}
	const loadPublicationByNomenclature = async parameters => {
		try {
			let response =
				await apiClient.publicationByNomenclature.read(parameters)

			publicationByNomenclature.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByNomenclature()
		}
	}
	const loadFifthAreaDocumentsStatisticsByQuarter = async parameters => {
		try {
			const { districts } = await apiClient.statistics.read(parameters)
			console.log('loadFifthAreaDocumentsStatisticsByQuarter', districts)

			// Используем flatMap для упрощения сбора данных
			fifthAreaStatistics.value = districts
				.flatMap(district =>
					district.regions.map(region => ({
						name: region.name,
						count: region.count,
					})),
				)
				.sort((a, b) => b.count - a.count) // Сортировка по убыванию
				.slice(0, 15)
				.sort((a, b) => a.count - b.count) // Обрезаем до 10 элементов
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropFifthAreaDocumentsStatisticsByQuarter()
		}
	}
	const loadSixthAreaDocumentsStatisticsByQuarter = async parameters => {
		try {
			const { districts } = await apiClient.statistics.read(parameters)
			console.log('loadSixthAreaDocumentsStatisticsByQuarter', districts)

			// Используем flatMap для упрощения сбора данных
			sixthAreaStatistics.value = districts
				.flatMap(district =>
					district.regions.map(region => ({
						name: region.name,
						count: region.count,
					})),
				)
				.sort((a, b) => a.count - b.count) // Сортировка по убыванию
				.slice(0, 15) // Обрезаем до 10 элементов
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropSixthAreaDocumentsStatisticsByQuarter()
		}
	}
	return {
		thirdAreaStatistics,
		getRegionsInDistrict,
		getAllStatistics,
		getStatistics,
		getDistricts,
		getPublicationByYears,
		getSecondAreaDocumentsStatisticsByMonth,
		getPublicationByNomenclature,
		getFifthAreaDocumentsStatisticsByQuarter,
		getSixthAreaDocumentsStatisticsByQuarter,

		dropPublicationByYears,
		dropSecondAreaDocumentsStatisticsByMonth,
		dropPublicationByNomenclature,
		dropFifthAreaDocumentsStatisticsByQuarter,
		dropSixthAreaDocumentsStatisticsByQuarter,

		loadPublicationByYears,
		loadSecondAreaDocumentsStatisticsByMonth,
		loadPublicationByNomenclature,
		loadFifthAreaDocumentsStatisticsByQuarter,
		loadSixthAreaDocumentsStatisticsByQuarter,

		setStatistics,
		dropStatistics,
		loadStatisticsAPI,
		updateStatisticsAPI,

		getPublicationByNomenclatureSeries,
		getPublicationByNomenclatureLabels,

		getPublicationByYearsSeries,
		getPublicationByYearsLabels,
	}
})
