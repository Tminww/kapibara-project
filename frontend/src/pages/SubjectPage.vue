<template>
	<v-navigation-drawer
		location="left"
		temporary
		:width="450"
		elevation="10"
		v-model="leftMenu"
		permanent=""
		:rail="rail"
		@click="rail = false"
	>
		<v-list-item nav>
			<v-list-item-title
				><h2 class="font-weight-bold pl-2">
					Выбрать регионы
				</h2></v-list-item-title
			>
			<template v-slot:append>
				<v-btn
					icon="mdi-chevron-left"
					variant="text"
					@click.stop="leftMenu = !leftMenu"
				></v-btn>
			</template>
		</v-list-item>

		<v-divider></v-divider>

		<v-container>
			<div v-if="errorSubjects">
				<v-alert
					class="d-flex align-center justify-center"
					type="error"
					title="Произошла ошибка"
					:text="errorSubjects"
					variant="tonal"
				></v-alert>
			</div>
			<template v-else>
				<div
					v-if="loadingSubjests"
					class="d-flex align-center justify-center"
				>
					<v-progress-circular indeterminate />
				</div>

				<template v-else>
					<t-filter-form
						:districts="subjectStore.getRegionsToRequest"
					/>
				</template>
			</template>
		</v-container>
	</v-navigation-drawer>

	<v-container>
		<v-btn
			color="primary"
			variant="tonal"
			rounded
			@click="leftMenu = !leftMenu"
		>
			Фильтры</v-btn
		>
		<v-row no-gutters>
			<v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isThirdAreaLoading"
						:min-width="500"
						:max-width="700"
						title="Опубликование по Федеральным округам"
					>
						<template #chart>
							<v-date-input
								class="mb-2"
								v-model="rangeDates"
								variant="outlined"
								prepend-icon=""
								prepend-inner-icon=""
								label="Выбрать временной интервал"
								max-width="360"
								multiple="range"
								hide-details
								rounded
								density="compact"
								placeholder="DD.MM.YYYY - DD.MM.YYYY"
								@update:model-value="onSubmit"
							></v-date-input>
							<div class="button-group-wrap">
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый месяц</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый квартал</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый год</v-btn
								>
							</div>
							<t-skeleton-donut-chart
								v-if="isThirdAreaLoading"
							></t-skeleton-donut-chart>

							<t-donut-chart
								v-else
								:labels="thirdAreaLabels"
								:series="thirdAreaSeries"
								:is-legend-clickable="true"
								:height="410"
							/>
						</template>

						<template #error> {{ thirdAreaError }}</template>
					</t-dashboard-area-card>
				</v-container> </v-col
			><v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isFirstAreaLoading"
						:min-width="700"
						:max-width="700"
						title="Опубликование всех нормативных правовых актов"
					>
						<template #chart>
							<v-date-input
								class="mb-2"
								v-model="rangeDates"
								variant="outlined"
								prepend-icon=""
								prepend-inner-icon=""
								label="Выбрать временной интервал"
								max-width="360"
								multiple="range"
								hide-details
								rounded
								density="compact"
								placeholder="DD.MM.YYYY - DD.MM.YYYY"
								@update:model-value="onSubmit"
							></v-date-input>
							<div class="button-group-wrap">
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый месяц</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый квартал</v-btn
								>
								<v-btn color="primary" variant="tonal" rounded
									>Прошлый год</v-btn
								>
							</div>

							<t-skeleton-column-chart
								v-if="isFirstAreaLoading"
							></t-skeleton-column-chart>

							<t-column-chart
								v-else
								:labels="firstAreaLabels"
								:series="firstAreaSeries"
								:height="410"
							/>
						</template>
						<template #error> {{ thirdAreaError }}</template>
					</t-dashboard-area-card>
				</v-container>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue'
	import { TDashboardAreaCard, TFilterForm } from '@/components/widgets'
	import { VDateInput } from 'vuetify/labs/VDateInput'
	import { useSubjectStore } from '@/stores'
	import {
		TDonutChart,
		TSkeletonDonutChart,
		TColumnChart,
		TSkeletonColumnChart,
	} from '@/components/widgets'
	import { useSubjectDashboardArea } from '@/composables/useSubjectDashboardArea'
	import { useFirstDashboardArea } from '@/composables/useFirstDashboartArea'

	import { useDate } from 'vuetify'

	const date = useDate()
	const loadingSubjects = ref(false)
	const errorSubjects = ref(null)
	const leftMenu = ref(false)
	const rail = ref(false)
	const resultIsEmpty = ref(false)

	const subjectStore = useSubjectStore()

	const emptyRequest = computed(() => {
		return resultIsEmpty.value
	})
	const loadSubjects = async () => {
		try {
			loadingSubjects.value = true
			errorSubjects.value = null
			await subjectStore.loadSubjectsAPI()
		} catch (e) {
			errorSubjects.value = e.message
			subjectStore.dropRegionsToRequest()
		} finally {
			loadingSubjects.value = false
		}
	}

	onMounted(async () => {
		await loadSubjects()
	})
	const rangeDates = ref([])

	const getEndsOfDateRange = computed(() => {
		const startDate = rangeDates.value.at(0)
		const endDate = rangeDates.value.at(-1)

		return {
			startDate: date.format(startDate, 'keyboardDate'),
			endDate: date.format(endDate, 'keyboardDate'),
		}
	})

	const onSubmit = async () => {
		console.log('onSubmit', getEndsOfDateRange.value)
	}
	const rules = ref({
		required: value => !!value || 'Field is required',
	})
	const {
		firstAreaLabels,
		firstAreaSeries,
		firstAreaError,
		firstAreaYear,
		isFirstAreaPreviousLoading,
		isFirstAreaNextLoading,
		isFirstAreaLoading,
		firstAreaPreviousYear,
		firstAreaNextYear,
	} = useFirstDashboardArea()

	const {
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
	} = useSubjectDashboardArea()
</script>

<style scoped>
	.button-group-wrap {
		display: flex;
		align-items: center; /* Выравнивание элементов по центру */
		gap: 5px; /* Отступ между иконкой и текстом */
	}
</style>
