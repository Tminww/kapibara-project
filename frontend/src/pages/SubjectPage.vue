<template>
	<v-container>
		<v-row no-gutters
			><v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isFirstAreaLoading"
						:min-width="300"
						:max-width="580"
						title="Опубликование всех нормативных правовых актов"
					>
						<template #chart>
							<v-date-input
								class="mb-2"
								v-model="rangeDates"
								variant="outlined"
								prepend-icon=""
								prepend-inner-icon=""
								label="Выбрать период"
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
								:height="400"
							/>
						</template>
						<!-- <template #previous>
						<v-btn
							color="primary"
							:loading="isFirstAreaPreviousLoading"
							@click="firstAreaPreviousYear"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isFirstAreaNextLoading"
							@click="firstAreaNextYear"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template> -->
						<!-- <template #quarter>
						
					</template> -->
						<template #error> {{ thirdAreaError }}</template>
					</t-dashboard-area-card>
				</v-container>
			</v-col>

			<v-col cols="auto">
				<v-container>
					<t-dashboard-area-card
						:isLoading="isThirdAreaLoading"
						:min-width="300"
						:max-width="580"
						title="Опубликование по Федеральным округам"
					>
						<template #chart>
							<v-date-input
								class="mb-2"
								v-model="rangeDates"
								variant="outlined"
								prepend-icon=""
								prepend-inner-icon=""
								label="Выбрать период"
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
								:height="300"
							/>
						</template>
						<template #previous>
							<v-btn
								color="primary"
								:loading="isThirdAreaPreviousLoading"
								@click="thirdAreaPreviousQuarter"
							>
								<v-icon>mdi-arrow-left</v-icon>
							</v-btn>
						</template>
						<template #next
							><v-btn
								color="primary"
								:loading="isThirdAreaNextLoading"
								@click="thirdAreaNextQuarter"
							>
								<v-icon>mdi-arrow-right</v-icon>
							</v-btn>
						</template>
						<template #quarter v-if="!isThirdAreaLoading">
							{{ thirdAreaQuarter.startDate }} -
							{{ thirdAreaQuarter.endDate }}
						</template>
						<template #error> {{ thirdAreaError }}</template>
					</t-dashboard-area-card>
				</v-container>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
	import { ref, computed } from 'vue'
	import { TDashboardAreaCard } from '@/components/widgets'
	import { VDateInput } from 'vuetify/labs/VDateInput'

	import {
		TDonutChart,
		TSkeletonDonutChart,
		TColumnChart,
		TSkeletonColumnChart,
	} from '@/components/widgets'
	import { useFirstDashboardArea } from '@/composables/useFirstDashboartArea'
	import { useSecondDashboardArea } from '@/composables/useSecondDashboardArea'
	import { useThirdDashboardArea } from '@/composables/useThirdDashboardArea'
	import { useFourthDashboardArea } from '@/composables/useFourthDashboardArea'
	import { useFifthDashboardArea } from '@/composables/useFifthDashboardArea'
	import { useSixthDashboardArea } from '@/composables/useSixthDashboardArea'

	import { useDate } from 'vuetify'

	const date = useDate()
	const formatted = date.format('2010-04-13', 'keyboardDate')

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
		secondAreaLabels,
		secondAreaSeries,
		secondAreaError,
		secondAreaDate,
		secondAreaMonth,
		isSecondAreaPreviousLoading,
		isSecondAreaNextLoading,
		isSecondAreaLoading,
		secondAreaPreviousMonth,
		secondAreaNextMonth,
	} = useSecondDashboardArea()

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
	} = useThirdDashboardArea()
	const {
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
	} = useFourthDashboardArea()

	const {
		fifthAreaLabels,
		fifthAreaSeries,
		fifthAreaError,
		fifthAreaDate,
		fifthAreaQuarter,
		isFifthAreaPreviousLoading,
		isFifthAreaNextLoading,
		isFifthAreaLoading,
		fifthAreaPreviousQuarter,
		fifthAreaNextQuarter,
	} = useFifthDashboardArea()
	const {
		sixthAreaLabels,
		sixthAreaSeries,
		sixthAreaError,
		sixthAreaDate,
		sixthAreaQuarter,
		isSixthAreaPreviousLoading,
		isSixthAreaNextLoading,
		isSixthAreaLoading,
		sixthAreaPreviousQuarter,
		sixthAreaNextQuarter,
	} = useSixthDashboardArea()
</script>

<style scoped>
	.button-group-wrap {
		display: flex;
		align-items: center; /* Выравнивание элементов по центру */
		gap: 5px; /* Отступ между иконкой и текстом */
	}
</style>
