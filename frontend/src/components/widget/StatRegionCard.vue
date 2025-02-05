<template>
	<v-card class="mx-auto" elevation="8" max-width="500" hover>
		<v-toolbar
			dense
			flat
			class="text-h6 mb-1 px-4"
			color="primary lighten-2"
			>{{ region.name }}
		</v-toolbar>
		<v-card-title class="text-h6 mb-1">
			Всего НПА: {{ region.count }}
		</v-card-title>

		<v-card-text>
			<div class="justify-center">
				<doughnut-chart v-if="loaded" :chartData :chartOptions />
			</div>
		</v-card-text>
	</v-card>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue'
	import DoughnutChart from './DoughnutChart.vue'

	const props = defineProps({
		region: { type: Object, required: true },
	})

	const loaded = ref(false)

	const chartOptions = computed(() => {
		let categories = []

		for (const row of props.region.stat) {
			categories.push(row.name)
		}
		return [
			{
				chart: {
					id: 'vuechart-stat-all-card',
				},
				xaxis: {
					categories,
				},
			},
		]
	})
	const chartData = computed(() => {
		let data = []

		for (const row of props.region.stat) {
			data.push(row.count)
		}

		return {
			name: 'series-1',
			data,
		}
	})

	onMounted(() => {
		console.log('REGION', props.region)
		loaded.value = true
	})
</script>
<style scoped></style>
