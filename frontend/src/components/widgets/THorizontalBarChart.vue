<template>
	<t-base-chart :data> </t-base-chart>
</template>

<script setup>
	import { computed } from 'vue'
	import { TBaseChart } from '@/components/widgets'
	import { createHorizontalBarChartConfig } from '@/utils/horizontalBarChartConfig'

	const props = defineProps({
		labels: { type: Array, required: true },
		series: { type: Array, required: true },
	})

	const data = computed(() => {
		return createHorizontalBarChartConfig({
			labels: props.labels,
			series: props.series,
		})
	})
</script>
