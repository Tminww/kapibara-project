<template>
	<v-row>
		<v-col>
			<v-container>
				<t-dashboard-area-card
					:isLoading="isStatisticsLoading"
					:title="'Опубликование в ' + route.params.label"
					subtitle="За квартал"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isFourthAreaLoading"
						></t-skeleton-donut-chart>

						<t-donut-chart
							v-else
							:labels="labelsDistricts"
							:series="seriesDistricts"
						/>
					</template>
					<template #previous> </template>
					<template #next> </template>
					<template #quarter v-if="!isStatisticsLoading"> </template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import {
		THorizontalBarChart,
		TDonutChart,
		TSkeletonDonutChart,
	} from '@/components/widgets'
	import { TDashboardAreaCard } from '@/components/widgets'
	import { useRoute, useRouter } from 'vue-router'
	import { mapDistrictShortNameToName } from '@/utils/utils.js'
	import { useSubjectStore } from '@/stores'
	import { computed, ref, onMounted } from 'vue'
	const route = useRoute()
	const router = useRouter()
	const subjectStore = useSubjectStore()

	const errorStatistics = ref(null)
	const isStatisticsLoading = ref(false)

	const currentDistrictStat = computed(() => {
		const data = subjectStore.getDistricts
		for (districts of data) {
			console.log(districts)
		}
	})
	console.log(route.params.label)

	const loadStatistics = async () => {
		try {
			errorStatistics.value = null
			isStatisticsLoading.value = true
			const parameters = getLastQuarter()

			await subjectStore.loadSubjectStatisticsAPI(parameters)
		} catch (e) {
			errorStatistics.value = e.message
			subjectStore.dropStatistics()
		} finally {
			// setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
			isStatisticsLoading.value = false
		}
	}

	onMounted(async () => {
		await loadStatistics()
	})
</script>
