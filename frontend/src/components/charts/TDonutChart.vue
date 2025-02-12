<template>
	<t-base-chart :data :height> </t-base-chart>
</template>

<script setup>
	import { computed } from 'vue'
	import { TBaseChart } from '@/components/charts'
	import { createDonutChartConfig } from '@/utils/donutChartConfig'
	import { useRouter } from 'vue-router'

	const router = useRouter()

	const props = defineProps({
		labels: { type: Array, required: true },
		series: { type: Array, required: true },
		height: { type: Number, required: false },
		isLegendClickable: { type: Boolean, default: false },
	})

	const data = computed(() => {
		return createDonutChartConfig({
			labels: props.labels,
			series: props.series,
			isLegendClickable: props.isLegendClickable,
			router,
		})
	})
</script>
