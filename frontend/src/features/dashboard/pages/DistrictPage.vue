<template>
	<!-- Фильтры в боковом меню -->
	<t-filter-sidebar
		v-model="leftMenu"
		:rail="rail"
		:loadingSubjects="loadingSubjects"
		:errorSubjects="errorSubjects"
		:regions="store.getSubjects"
		@update:rail="rail = $event"
	/>

	<v-container>
		<v-btn
			color="primary"
			variant="tonal"
			rounded
			@click="leftMenu = !leftMenu"
		>
			Фильтры
		</v-btn>
	</v-container>
	<v-container>
		<v-row class="mt-2 justify-space-around">
			<v-col cols="auto">
				<t-area-card
					:title="store.getDistrictName"
					:is-loading="isLoading"
					:min-width="370"
					:max-width="370"
				>
					<template #chart>
						<t-icon
							v-if="isLoading"
							name="dashboard"
							:width="80"
							:height="80"
						/>
						<t-donut-chart
							v-else
							:labels="
								store.getDistrictStat.map(item => item.name)
							"
							:series="
								store.getDistrictStat.map(item => item.count)
							"
							:height="350"
							:enable-logarithmic="false"
							:log-base="10"
							:y-start-value="0"
							legend-position="bottom"
						/>
					</template>
					<template #interval v-if="!isLoading">
						{{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }}
						-
						{{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
					</template>
				</t-area-card>
			</v-col>
			<v-col cols="auto" v-for="region of store.getRegions" :key="region">
				<t-area-card
					:title="region.name"
					:is-loading="isLoading"
					:min-width="370"
					:max-width="370"
				>
					<template #chart>
						<t-icon
							v-if="isLoading"
							name="dashboard"
							:width="80"
							:height="80"
						/>
						<t-donut-chart
							v-else
							:labels="region?.stat?.map(item => item.name)"
							:series="region?.stat?.map(item => item.count)"
							:height="350"
							:enable-logarithmic="false"
							:log-base="10"
							:y-start-value="0"
							legend-position="bottom"
						/>
					</template>
					<template #interval v-if="!isLoading">
						{{ dateFormat(store.getStartDate, 'DD.MM.YYYY') }} -
						{{ dateFormat(store.getEndDate, 'DD.MM.YYYY') }}
					</template>
				</t-area-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { TIcon } from '@/components/ui'
	import {
		TAreaCard,
		TDonutChart,
		THorizontalBarChart,
		TColumnChart,
		TFilterSidebar,
	} from '../components/widgets'

	import { useDistrictStore } from '../stores/district'
	import {
		getLastMonth,
		getLastQuarter,
		getLastYear,
		getLastWeek,
		dateFormat,
	} from '@/utils/utils'
	import { computed, ref, onMounted } from 'vue'
	import { toast } from 'vue-sonner'
	import { useRoute, useRouter } from 'vue-router'
	const route = useRoute()

	const leftMenu = ref(false)
	const rail = ref(false)

	const store = useDistrictStore()

	const loadingSubjects = ref(false)
	const errorSubjects = ref(null)
	const loadingStatistics = ref(false)
	const errorStatistics = ref(null)

	const isLoading = computed(() => {
		return store.isLoading || loadingStatistics.value
	})

	const loadStatistics = async () => {
		try {
			loadingStatistics.value = true
			errorStatistics.value = null
			console.log('FUNC', getLastMonth())

			const parameters = getLastMonth()
			parameters.regions = store.getSubjects.map(s => s.id).toString()
			await store.loadStatisticsAPI(route.params.label, parameters)
		} catch (e) {
			errorStatistics.value = e.message
			store.dropStatistics()
		} finally {
			loadingStatistics.value = false
		}
	}

	const loadSubjects = async () => {
		try {
			loadingSubjects.value = true
			errorSubjects.value = null
			await store.loadSubjectsAPI(route.params.label)
		} catch (e) {
			errorSubjects.value = e.message
			store.dropRegionsToRequest()
		} finally {
			loadingSubjects.value = false
		}
	}

	onMounted(async () => {
		loadingStatistics.value = true
		await loadSubjects()

		await loadStatistics()
		loadingStatistics.value = false
	})
</script>

<style scoped></style>
