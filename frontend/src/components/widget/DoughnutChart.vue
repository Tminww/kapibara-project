<template>
	<apexchart
		v-if="chartData"
		width="500"
		type="bar"
		:options="chartOptions"
		:series="chartData"
	></apexchart>
	<template v-else>
		<v-progress-circular indeterminate />
	</template>
</template>

<script setup>
	import { defineProps } from 'vue'

	const props = defineProps({
		chartData: {
			type: Object,
			required: true,
		},
		chartOptions: {
			type: Array,
			default: () => [],
		},
	})
</script>
