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
	const publicationByNomenclatureDetail = ref({ ...emptyResponse })

	const publicationByRegionsMin = ref({ ...emptyResponse })
	const publicationByRegionsMax = ref({ ...emptyResponse })

	const publicationByDistricts = ref({ ...emptyResponse })

	const getPublicationByDistricts = computed(() => {
		return publicationByDistricts.value.stat
	})

	const getPublicationByDistrictsSeries = computed(() => {
		return publicationByDistricts.value?.stat?.map(row => row.count)
	})

	const getPublicationByDistrictsLabels = computed(() => {
		return publicationByDistricts.value?.stat?.map(row => row.name)
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

	const getPublicationByNomenclatureDetail = computed(() => {
		return publicationByNomenclatureDetail.value.stat
	})

	const getPublicationByNomenclatureDetailSeries = computed(() => {
		return publicationByNomenclatureDetail.value?.stat
			?.filter(row => row.count !== 0) // Пропускаем строки с count == 0
			?.map(row => row.count) // Извлекаем только count
	})

	const getPublicationByNomenclatureDetailLabels = computed(() => {
		return publicationByNomenclatureDetail.value?.stat
			?.filter(row => row.count !== 0) // Пропускаем строки с count == 0
			?.map(row => row.name) // Извлекаем только count
	})

	const getPublicationByNomenclatureDetailTotal = computed(() => {
		return publicationByNomenclatureDetail.value?.count
	})

	const getPublicationByRegionsMin = computed(() => {
		return publicationByRegionsMin.value.stat
	})

	const getPublicationByRegionsMinSeries = computed(() => {
		return publicationByRegionsMin.value?.stat?.map(row => row.count)
	})

	const getPublicationByRegionsMinLabels = computed(() => {
		return publicationByRegionsMin.value?.stat?.map(row => row.name)
	})
	const getPublicationByRegionsMax = computed(() => {
		return publicationByRegionsMax.value.stat
	})

	const getPublicationByRegionsMaxSeries = computed(() => {
		return publicationByRegionsMax.value?.stat?.map(row => row.count)
	})

	const getPublicationByRegionsMaxLabels = computed(() => {
		return publicationByRegionsMax.value?.stat?.map(row => row.name)
	})

	const dropPublicationByYears = () => {
		publicationByYears.value = { ...emptyResponse }
	}

	const dropPublicationByDistricts = () => {
		publicationByDistricts.value = { ...emptyResponse }
	}
	const dropSecondAreaDocumentsStatisticsByMonth = () => {
		secondAreaStatistics.value = []
	}
	const dropPublicationByNomenclature = () => {
		publicationByNomenclature.value = { ...emptyResponse }
	}
	const dropPublicationByNomenclatureDetail = () => {
		publicationByNomenclatureDetail.value = { ...emptyResponse }
	}
	const dropPublicationByRegionsMin = () => {
		publicationByRegionsMin.value = { ...emptyResponse }
	}
	const dropPublicationByRegionsMax = () => {
		publicationByRegionsMax.value = { ...emptyResponse }
	}

	// Обновление статистики через API
	const loadPublicationByDistricts = async parameters => {
		try {
			let response =
				await apiClient.publicationByDistricts.read(parameters)

			publicationByDistricts.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByDistricts()
		}
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
	const loadPublicationByNomenclatureDetail = async parameters => {
		try {
			let response =
				await apiClient.publicationByNomenclatureDetail.read(parameters)

			publicationByNomenclatureDetail.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByNomenclatureDetail()
		}
	}
	const loadPublicationByRegionsMin = async parameters => {
		try {
			parameters.sort = 'min'
			parameters.limit = 10

			let response = await apiClient.publicationByRegions.read(parameters)

			publicationByRegionsMin.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByRegionsMin()
		}
	}
	const loadPublicationByRegionsMax = async parameters => {
		try {
			parameters.sort = 'max'
			parameters.limit = 10

			let response = await apiClient.publicationByRegions.read(parameters)

			publicationByRegionsMax.value = response
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropPublicationByRegionsMax()
		}
	}
	return {
		getPublicationByYears,
		getSecondAreaDocumentsStatisticsByMonth,
		getPublicationByNomenclature,
		getPublicationByNomenclatureDetail,
		getPublicationByRegionsMin,
		getPublicationByRegionsMax,
		getPublicationByDistricts,

		dropPublicationByYears,
		dropSecondAreaDocumentsStatisticsByMonth,
		dropPublicationByNomenclature,
		dropPublicationByNomenclatureDetail,

		dropPublicationByRegionsMin,
		dropPublicationByRegionsMax,
		dropPublicationByDistricts,

		loadPublicationByYears,
		loadSecondAreaDocumentsStatisticsByMonth,
		loadPublicationByNomenclature,
		loadPublicationByNomenclatureDetail,

		loadPublicationByRegionsMin,
		loadPublicationByRegionsMax,
		loadPublicationByDistricts,

		getPublicationByNomenclatureSeries,
		getPublicationByNomenclatureDetailSeries,
		getPublicationByYearsSeries,
		getPublicationByDistrictsSeries,
		getPublicationByRegionsMinSeries,
		getPublicationByRegionsMaxSeries,

		getPublicationByNomenclatureLabels,
		getPublicationByNomenclatureDetailLabels,
		getPublicationByYearsLabels,
		getPublicationByDistrictsLabels,
		getPublicationByRegionsMinLabels,
		getPublicationByRegionsMaxLabels,

		getPublicationByNomenclatureDetailTotal,
	}
})
