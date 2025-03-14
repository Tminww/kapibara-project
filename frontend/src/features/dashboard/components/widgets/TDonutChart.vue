<template>
	<t-base-chart :data :height> </t-base-chart>
</template>

<script setup>
	import { computed } from 'vue'
	import { TBaseChart } from './'
	import { createDonutChartConfig } from '../../utils/donutChartConfig'
	import { useRouter } from 'vue-router'

	const router = useRouter()

	const props = defineProps({
		labels: { type: Array, required: true },
		series: { type: Array, required: true },
		height: { type: Number, required: false },
		legendPosition: {
			type: String,
			default: 'left',
			validators: ['top', 'bottom', 'left', 'right'],
		},
		isLegendClickable: { type: Boolean, default: false },
		routeName: { type: String, default: 'region' },
	})

	const data = computed(() => {
		return createDonutChartConfig({
			labels: props.labels,
			series: props.series,
			isLegendClickable: props.isLegendClickable,
			legendPosition: props.legendPosition,
			router,
			routeName: props.routeName,
		})
	})
</script>
