import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

import { useSubjectStore } from '@/stores/'
import { getLastQuarter, mapDistrictNameToShortName } from '@/utils/utils.js'

export function useSubjectDashboardArea() {
	const subjectStore = useSubjectStore()
	const thirdAreaError = ref(null)
	const thirdAreaDate = ref(new Date())
	const isThirdAreaPreviousLoading = ref(false)
	const isThirdAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isThirdAreaLoading = computed(() => {
		return subjectStore.isLoading || isStatisticsLoading.value
	})
	const thirdAreaQuarter = computed(() => {
		const { startDate, endDate } = getLastQuarter(thirdAreaDate.value)
		console.log('ThirdAreaQuarter', startDate, endDate)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')
		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const districtData = computed(() =>
		Array.isArray(subjectStore.getDistricts)
			? subjectStore.getDistricts
			: [],
	)

	const thirdAreaSeries = computed(() =>
		districtData.value.map(row => row.count),
	)

	const thirdAreaLabels = computed(() =>
		districtData.value.map(row => mapDistrictNameToShortName(row.name)),
	)

	const thirdAreaPreviousQuarter = async () => {
		try {
			thirdAreaError.value = null
			isThirdAreaPreviousLoading.value = true
			thirdAreaDate.value = new Date(
				thirdAreaDate.value.setMonth(
					thirdAreaDate.value.getMonth() - 3,
				),
			)

			const parameters = getLastQuarter(thirdAreaDate.value)

			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			thirdAreaError.value = e.message
		} finally {
			isThirdAreaPreviousLoading.value = false
		}
	}

	const thirdAreaNextQuarter = async () => {
		try {
			thirdAreaError.value = null
			isThirdAreaNextLoading.value = true
			if (thirdAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			thirdAreaDate.value = new Date(
				thirdAreaDate.value.setMonth(
					thirdAreaDate.value.getMonth() + 3,
				),
			)

			const parameters = getLastQuarter(thirdAreaDate.value)

			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			thirdAreaError.value = e.message
		} finally {
			isThirdAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			thirdAreaError.value = null
			isStatisticsLoading.value = true

			const parameters = getLastQuarter()

			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			thirdAreaError.value = e.message
			subjectStore.dropStatistics()
		} finally {
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})

	return {
		thirdAreaLabels,
		thirdAreaSeries,
		thirdAreaError,
		thirdAreaDate,
		thirdAreaQuarter,
		isThirdAreaPreviousLoading,
		isThirdAreaNextLoading,
		isThirdAreaLoading,
		thirdAreaPreviousQuarter,
		thirdAreaNextQuarter,
	}
}
