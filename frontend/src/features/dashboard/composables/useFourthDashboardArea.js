import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue-sonner'

import { useDashboardStore } from '../store'
import { getLastYear } from '@/utils/utils'

export function useFourthDashboardArea() {
	const statisticStore = useDashboardStore()
	const fourthAreaError = ref(null)
	const fourthAreaDate = ref(new Date())
	const isFourthAreaPreviousLoading = ref(false)
	const isFourthAreaNextLoading = ref(false)
	const isStatisticsLoading = ref(false)

	const isFourthAreaLoading = computed(() => {
		return (
			isFourthAreaPreviousLoading.value ||
			isFourthAreaNextLoading.value ||
			isStatisticsLoading.value
		)
	})
	const fourthAreaYear = computed(() => {
		console.log(fourthAreaDate.value)

		const { startDate, endDate } = getLastYear(fourthAreaDate.value)
		console.log('FourthAreaYear', startDate, endDate)
		const [startYear, startMonth, startDay] = startDate.split('-')

		const [endYear, endMonth, endDay] = endDate.split('-')
		console.table({
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		})
		return {
			startDate: `${startDay}.${startMonth}.${startYear}`,
			endDate: `${endDay}.${endMonth}.${endYear}`,
		}
	})
	const data = computed(() =>
		Array.isArray(statisticStore.getFourthAreaDocumentsStatisticsByYear)
			? statisticStore.getFourthAreaDocumentsStatisticsByYear
			: [],
	)

	const fourthAreaSeries = computed(() => data.value.map(row => row.count))

	const fourthAreaLabels = computed(() =>
		data.value.map(row => row.shortName),
	)

	const fourthAreaPreviousYear = async () => {
		try {
			fourthAreaError.value = null
			isFourthAreaPreviousLoading.value = true
			fourthAreaDate.value = new Date(
				fourthAreaDate.value.setFullYear(
					fourthAreaDate.value.getFullYear() - 1,
				),
			)

			const parameters = getLastYear(fourthAreaDate.value)

			await statisticStore.loadFourthAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			fourthAreaError.value = e.message
		} finally {
			isFourthAreaPreviousLoading.value = false
		}
	}

	const fourthAreaNextYear = async () => {
		try {
			fourthAreaError.value = null
			isFourthAreaNextLoading.value = true
			if (fourthAreaDate.value >= new Date()) {
				toast.warning('Нельзя переходить в будущее')
				return
			}
			fourthAreaDate.value = new Date(
				fourthAreaDate.value.setFullYear(
					fourthAreaDate.value.getFullYear() + 1,
				),
			)

			const parameters = getLastYear(fourthAreaDate.value)

			await statisticStore.loadFourthAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			fourthAreaError.value = e.message
		} finally {
			isFourthAreaNextLoading.value = false
		}
	}

	const loadStatistics = async () => {
		try {
			fourthAreaError.value = null
			isStatisticsLoading.value = true

			const parameters = getLastYear()

			await statisticStore.loadFourthAreaDocumentsStatisticsByYear(
				parameters,
			)
		} catch (e) {
			fourthAreaError.value = e.message
			statisticStore.dropStatistics()
		} finally {
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})

	return {
		fourthAreaLabels,
		fourthAreaSeries,
		fourthAreaError,
		fourthAreaDate,
		fourthAreaYear,
		isFourthAreaPreviousLoading,
		isFourthAreaNextLoading,
		isFourthAreaLoading,
		fourthAreaPreviousYear,
		fourthAreaNextYear,
	}
}
