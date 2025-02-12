<template>
	<v-row no-gutters
		><v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFirstAreaLoading"
					title="Опубликование всех нормативных правовых актов"
					subtitle="За год"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isFirstAreaLoading"
						></t-skeleton-column-chart>

						<t-column-chart
							v-else
							:labels="firstAreaLabels"
							:series="firstAreaSeries"
							:height="240"
						/>
					</template>
					<template #previous>
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
					</template>
					<template #quarter v-if="!isThirdAreaLoading">
						{{ firstAreaYear.startDate }} -
						{{ firstAreaYear.endDate }}
					</template>
					<template #error> {{ thirdAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isSecondAreaLoading"
					title="Статистика опубликования всех нормативных правовых актов"
					subtitle="За месяц"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isSecondAreaLoading"
						></t-skeleton-column-chart>

						<t-column-chart
							v-else
							:labels="secondAreaLabels"
							:series="secondAreaSeries"
							:height="240"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isSecondAreaPreviousLoading"
							@click="secondAreaPreviousMonth"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isSecondAreaNextLoading"
							@click="secondAreaNextMonth"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #quarter v-if="!isSecondAreaLoading">
						{{ secondAreaMonth.startDate }} -
						{{ secondAreaMonth.endDate }}
					</template>
					<template #error> {{ secondAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="4">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isThirdAreaLoading"
					title="Опубликование по Федеральным округам"
					subtitle="За квартал"
					:max-width="460"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isThirdAreaLoading"
						></t-skeleton-donut-chart>

						<t-donut-chart
							v-else
							:labels="thirdAreaLabels"
							:series="thirdAreaSeries"
							:is-legend-clickable="true"
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
		<v-col cols="4">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFourthAreaLoading"
					title="Опубликование по номенклатуре"
					subtitle="За год"
					:max-width="650"
				>
					<template #chart>
						<t-skeleton-donut-chart
							v-if="isFourthAreaLoading"
						></t-skeleton-donut-chart>

						<t-donut-chart
							v-else
							:labels="fourthAreaLabels"
							:series="fourthAreaSeries"
							:height="270"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isFourthAreaPreviousLoading"
							@click="fourthAreaPreviousYear"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isFourthAreaNextLoading"
							@click="fourthAreaNextYear"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #quarter v-if="!isFourthAreaLoading">
						{{ fourthAreaYear.startDate }} -
						{{ fourthAreaYear.endDate }}
					</template>
					<template #error> {{ fourthAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>

		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isSixthAreaLoading"
					title="Статистика субъектов РФ"
					subtitle="Минимальное за квартал"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isSixthAreaLoading"
						></t-skeleton-column-chart>

						<t-column-chart
							v-else
							:labels="sixthAreaLabels"
							:series="sixthAreaSeries"
							:log-base="10"
							:enable-logarithmic="false"
							:y-start-value="0"
							:height="240"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isSixthAreaPreviousLoading"
							@click="sixthAreaPreviousQuarter"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isSixthAreaNextLoading"
							@click="sixthAreaNextQuarter"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #quarter v-if="!isSixthAreaLoading">
						{{ sixthAreaQuarter.startDate }} -
						{{ sixthAreaQuarter.endDate }}
					</template>
					<template #error> {{ sixthAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
		<v-col cols="6">
			<v-container>
				<t-dashboard-area-card
					:isLoading="isFifthAreaLoading"
					title="Статистика субъектов РФ"
					subtitle="Максимальное за квартал"
				>
					<template #chart>
						<t-skeleton-column-chart
							v-if="isFifthAreaLoading"
						></t-skeleton-column-chart>

						<t-column-chart
							v-else
							:labels="fifthAreaLabels"
							:series="fifthAreaSeries"
							:log-base="10"
							:enable-logarithmic="false"
							:y-start-value="0"
							:height="240"
						/>
					</template>
					<template #previous>
						<v-btn
							color="primary"
							:loading="isFifthAreaPreviousLoading"
							@click="fifthAreaPreviousQuarter"
						>
							<v-icon>mdi-arrow-left</v-icon>
						</v-btn>
					</template>
					<template #next
						><v-btn
							color="primary"
							:loading="isFifthAreaNextLoading"
							@click="fifthAreaNextQuarter"
						>
							<v-icon>mdi-arrow-right</v-icon>
						</v-btn>
					</template>
					<template #quarter v-if="!isFifthAreaLoading">
						{{ fifthAreaQuarter.startDate }} -
						{{ fifthAreaQuarter.endDate }}
					</template>
					<template #error> {{ fifthAreaError }}</template>
				</t-dashboard-area-card>
			</v-container>
		</v-col>
	</v-row>
</template>

<script setup>
	import { TDashboardAreaCard } from '@/components/widgets'
	import {
		TDonutChart,
		TSkeletonDonutChart,
		TColumnChart,
		TSkeletonColumnChart,
	} from '@/components/charts'
	import { useFirstDashboardArea } from '@/composables/useFirstDashboartArea'
	import { useSecondDashboardArea } from '@/composables/useSecondDashboardArea'
	import { useThirdDashboardArea } from '@/composables/useThirdDashboardArea'
	import { useFourthDashboardArea } from '@/composables/useFourthDashboardArea'
	import { useFifthDashboardArea } from '@/composables/useFifthDashboardArea'
	import { useSixthDashboardArea } from '@/composables/useSixthDashboardArea'
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

<style scoped></style>
