<template>
	<v-card class="mx-auto" elevation="8" max-width="500" hover>
		<v-toolbar dense flat class="text-h6 mb-1 px-4" color="red lighten-2">
			{{ all.name }}
		</v-toolbar>
		<v-card-title class="text-h6 mb-1">
			Всего НПА: {{ all.count }}
		</v-card-title>

		<v-card-text>
			<div class="justify-center">
				<doughnut-chart v-if="loaded" :chart-data="this.chartData" :chart-options="this.chartOptions" />
			</div>
		</v-card-text>
	</v-card>
</template>

<script lang="js">
import DoughnutChart from './DoughnutChart.vue'
export default {
	name: 'stat-all-card',
	components: { DoughnutChart },
	props: {
		all: { type: Object, required: true },
	},
	data() {
		return {
			loaded: false,
		}
	},

	computed: {
		chartData() {
			let labels = []
			let data = []
			for (const row of this.all.stat) {
				labels.push(row.name)
				data.push(row.count)
			}
			return {
				labels,
				datasets: [
					{
						borderWidth: 2,
						backgroundColor: [
							'rgb(255, 99, 132)',
							'rgb(54, 162, 235)',
							'rgb(255, 205, 86)',
							'rgb(255, 99, 132)',
							'rgb(54, 99, 235)',
							'rgb(255, 99, 86)',
							'rgb(255, 99, 99)',
							'rgb(54, 162, 99)',
							'rgb(255, 205, 99)',
						],

						data,
					},
				],
			}
		},
		chartOptions() {
			return {
				responsive: true,
				layout: {
					padding: {
						left: 0,
						right: 0,
					},
				},
				plugins: {
					legend: {
						position: 'right',
						// display: false,
						labels: {
							font: {
								size: 14,
								family: 'Helvetica',

							},
						},
					},
				},
			}
		},
	},

	methods: {
		setup() {
			this.chartData
			this.chartOptions
		},
	},
	async mounted() {
		console.log('ALL', this.all)
		this.loaded = false
		this.setup()
		this.loaded = true
	},
}
</script>

<style scoped></style>
