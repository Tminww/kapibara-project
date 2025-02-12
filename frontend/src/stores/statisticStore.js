import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'
import { allDocumentTypes, allOrgans } from '@/mock'
import { toast } from 'vue-sonner'

export const useStatisticStore = defineStore('statistic', () => {
	const firstAreaStatistics = ref([])
	const secondAreaStatistics = ref([])
	const fourthAreaStatistics = ref([])
	const fifthAreaStatistics = ref([])
	const sixthAreaStatistics = ref([])

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

	const getFirstAreaDocumentsStatisticsByYear = computed(() => {
		return firstAreaStatistics.value
	})
	const getSecondAreaDocumentsStatisticsByMonth = computed(() => {
		return secondAreaStatistics.value
	})
	const getFourthAreaDocumentsStatisticsByYear = computed(() => {
		return fourthAreaStatistics.value
	})
	const getFifthAreaDocumentsStatisticsByQuarter = computed(() => {
		return fifthAreaStatistics.value
	})
	const getSixthAreaDocumentsStatisticsByQuarter = computed(() => {
		return sixthAreaStatistics.value
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
	const dropFirstAreaDocumentsStatisticsByYear = () => {
		firstAreaStatistics.value = []
	}
	const dropSecondAreaDocumentsStatisticsByMonth = () => {
		secondAreaStatistics.value = []
	}
	const dropFourthAreaDocumentsStatisticsByYear = () => {
		fourthAreaStatistics.value = []
	}
	const dropFifthAreaDocumentsStatisticsByQuarter = () => {
		fifthAreaStatistics.value = []
	}
	const dropSixthAreaDocumentsStatisticsByQuarter = () => {
		sixthAreaStatistics.value = []
	}

	// Загрузка статистики с API
	const loadStatisticsAPI = async () => {
		statistics.value = await apiClient.statistics.readOneRegion(12)
	}

	// Обновление статистики через API
	const updateStatisticsAPI = async parameters => {
		statistics.value = await apiClient.statistics.read(parameters)
	}
	// Обновление статистики через API
	const loadFirstAreaDocumentsStatisticsByYear = async parameters => {
		try {
			let allData = await apiClient.statistics.read(parameters)
			console.log('loadFirstAreaDocumentsStatisticsByYear', allData.stat)

			allData = allData.stat || [] // Проверяем, что `stat` существует

			let newData = [...allData] // Копируем данные вместо `join`

			// Проверяем и добавляем отсутствующие объекты
			// allDocumentTypes.forEach(docType => {
			// 	const exists = newData.some(data => data.name === docType.name)
			// 	if (!exists) {
			// 		newData.push({ name: docType.name, count: 0 })
			// 	}
			// })

			firstAreaStatistics.value = newData
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropFirstAreaDocumentsStatisticsByYear()
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
	const loadFourthAreaDocumentsStatisticsByYear = async parameters => {
		try {
			let subjectsData = await apiClient.statistics.read(parameters)
			console.log(
				'loadFourthAreaDocumentsStatisticsByYear',
				subjectsData.count,
			)

			subjectsData = [
				{
					id: '022fd55f-9f60-481e-a636-56d74b9ca759',
					name: 'Органы государственной власти субъектов Российской Федерации',
					shortName: 'ОГВ Субъектов РФ',
					code: 'subjects',
					description:
						'Законы и иные правовые акты субъектов Российской Федерации',
					count: subjectsData.count,
				},
			] || [
				{
					id: '022fd55f-9f60-481e-a636-56d74b9ca759',
					name: 'Органы государственной власти субъектов Российской Федерации',
					shortName: 'ОГВ Субъектов РФ',
					code: 'subjects',
					description:
						'Законы и иные правовые акты субъектов Российской Федерации',
					count: 0,
				},
			] // Проверяем, что `stat` существует

			let newData = [...subjectsData] // Копируем данные вместо `join`

			allOrgans.forEach(organ => {
				const exists = newData.some(data => data.code === organ.code)
				if (!exists) {
					newData.push({
						id: organ.id,
						name: organ.name,
						shortName: String(organ.shortName).includes(
							'Российской Федерации',
						)
							? String(organ.shortName).replace(
									'Российской Федерации',
									'РФ',
								)
							: organ.shortName,
						code: organ.code,
						description: organ.description,
						count: 0,
					})
				}
			})

			fourthAreaStatistics.value = newData
		} catch (error) {
			console.error('Ошибка при загрузке статистики:', error)
			dropFourthAreaDocumentsStatisticsByYear()
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
		statistics,
		getRegionsInDistrict,
		getAllStatistics,
		getStatistics,
		getDistricts,
		getFirstAreaDocumentsStatisticsByYear,
		getSecondAreaDocumentsStatisticsByMonth,
		getFourthAreaDocumentsStatisticsByYear,
		getFifthAreaDocumentsStatisticsByQuarter,
		getSixthAreaDocumentsStatisticsByQuarter,

		dropFirstAreaDocumentsStatisticsByYear,
		dropSecondAreaDocumentsStatisticsByMonth,
		dropFourthAreaDocumentsStatisticsByYear,
		dropFifthAreaDocumentsStatisticsByQuarter,
		dropSixthAreaDocumentsStatisticsByQuarter,

		loadFirstAreaDocumentsStatisticsByYear,
		loadSecondAreaDocumentsStatisticsByMonth,
		loadFourthAreaDocumentsStatisticsByYear,
		loadFifthAreaDocumentsStatisticsByQuarter,
		loadSixthAreaDocumentsStatisticsByQuarter,

		setStatistics,
		dropStatistics,
		loadStatisticsAPI,
		updateStatisticsAPI,
	}
})
