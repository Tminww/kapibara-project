<template>
	<t-base-chart :data :height> </t-base-chart>
</template>

<script setup>
	import { computed } from 'vue'
	import { TBaseChart } from './'
	import { createColumnChartConfig } from '@/utils/columnChartConfig'

	const props = defineProps({
		labels: { type: Array, required: true },
		series: { type: Array, required: true },
		height: { type: Number, required: false },
		logBase: { type: Number, default: 10 },
		enableLogarithmic: { type: Boolean, default: true },
		yStartValue: { type: Number, default: 0.5 },
		tickAmount: { type: Number, default: undefined },
	})

	const data = computed(() => {
		return createColumnChartConfig({
			labels: props.labels,
			series: props.series,
			logBase: props.logBase,
			enableLogarithmic: props.enableLogarithmic,
			yStartValue: props.yStartValue,
			tickAmount: props.tickAmount,
		})
	})
</script>
