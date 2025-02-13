<template>
	<div class="chart-wrap">
		<div id="chart">
			<apexchart
				:options="props.data.chartOptions"
				:series="props.data.series"
				:height="props.height"
			></apexchart>
		</div>
	</div>
</template>
<script setup>
	const props = defineProps({
		data: {
			type: Object,
			required: true,
		},
		height: { type: Number, required: false },
	})
</script>
