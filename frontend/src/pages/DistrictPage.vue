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

						<t-horizontal-bar-chart
							v-else
							:labels="labelsDistricts"
							:series="seriesDistricts"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="fourthAreaPreviousLoading"
							@click="fourthAreaPreviousQuarter"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next> </template>
					<template #quarter v-if="!isStatisticsLoading">
						<!-- {{ fourthAreaQuarter.startDate }} -
						{{ fourthAreaQuarter.endDate }} -->
					</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import {
		THorizontalBarChart,
		TSkeletonDonutChart,
	} from '@/components/charts'
	import { TDashboardAreaCard } from '@/components/widgets'
	import { useRoute, useRouter } from 'vue-router'
	import { mapDistrictNameToShortName } from '@/utils/utils.js'
	import { useStatisticStore } from '@/stores'
	import { computed, ref, onMounted } from 'vue'
	const route = useRoute()
	const router = useRouter()
	const statisticStore = useStatisticStore()

	const errorStatistics = ref(null)
	const isStatisticsLoading = computed(() => {
		return Object.keys(statisticStore.getStatistics).length == 0
			? true
			: false
	})

	const currentDistrictStat = computed(() => {
		const data = statisticStore.getDistricts
		for (districts of data) {
			console.log(districts)
		}
	})
	console.log(route.params.label)

	const loadStatistics = async () => {
		try {
			errorStatistics.value = null
			const parameters = getLastQuarter()

			await statisticStore.updateStatisticsAPI(parameters)
		} catch (e) {
			errorStatistics.value = e.message
			statisticStore.dropStatistics()
		} // setDefaultValue() // Раскомментируйте, если нужно сбрасывать значения}
	}

	onMounted(async () => {
		await loadStatistics()
	})
</script>
