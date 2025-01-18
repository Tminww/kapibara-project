<template>
	<v-card class="mx-auto" elevation="8" max-width="500" hover>
		<v-toolbar
			dense
			flat
			class="text-h6 mb-1 px-4"
			color="primary lighten-2"
			>{{ district.name }}
		</v-toolbar>
		<v-card-title class="text-h6 mb-1">
			Всего НПА: {{ district.count }}
		</v-card-title>

		<v-card-text>
			<div class="justify-center">
				<doughnut-chart
					v-if="loaded"
					:chart-data="this.chartData"
					:chart-options="this.chartOptions"
				/>
			</div>
		</v-card-text>

		<v-card-actions class="justify-center">
			<v-btn color="primary" @click="dialog = true"> Детально </v-btn>

			<v-dialog
				v-model="dialog"
				fullscreen
				transition="dialog-bottom-transition"
			>
				<v-card>
					<v-toolbar dark color="primary">
						<v-toolbar-title
							>Статистика в {{ shortName }} за {{ timeInterval }}
						</v-toolbar-title>
						<v-spacer></v-spacer>
						<v-toolbar-items>
							<v-btn icon dark @click="dialog = false">
								<v-icon>mdi-close</v-icon>
							</v-btn>
						</v-toolbar-items>
					</v-toolbar>
					<v-card-text>
						<v-row justify="center">
							<v-col v-for="region in this.district.regions">
								<stat-region-card :region="region" />
							</v-col>
						</v-row>
					</v-card-text>
					<v-card-actions>
						<v-btn color="primary" block @click="dialog = false"
							>Закрыть статистику
						</v-btn>
					</v-card-actions>
				</v-card>
			</v-dialog>
		</v-card-actions>
	</v-card>
</template>

<script lang="js">
	import DoughnutChart from './DoughnutChart.vue'
	import StatRegionCard from './StatRegionCard.vue'
	export default {
		name: 'stat-district-card',

		components: { DoughnutChart, StatRegionCard },
		props: {
			district: { type: Object, required: true },
			timeInterval: { type: String, required: true },
		},

		data() {
			return {
				loaded: false,
				dialog: false,
			}
		},
		computed: {
			shortName() {
				return this.getShortDistrictName(this.district.name)
			},
			chartData() {
				let labels = []
				let data = []
				for (const row of this.district.stat) {
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
			getShortDistrictName(fullName) {
				const districtAbbreviations = {
					'Центральный Федеральный округ': 'ЦФО',
					'Северо-Западный Федеральный округ': 'СЗФО',
					'Южный Федеральный округ': 'ЮФО',
					'Северо-Кавказский Федеральный округ': 'СКФО',
					'Приволжский Федеральный округ': 'ПФО',
					'Уральский Федеральный округ': 'УФО',
					'Сибирский Федеральный округ': 'СФО',
					'Дальневосточный Федеральный округ': 'ДФО',
				}
				return districtAbbreviations[fullName] || fullName
			},
		},
		async mounted() {
			console.log('DISTRICT', this.district)
			console.log('TIME', this.timeInterval)
			this.loaded = false
			this.setup()
			this.loaded = true
		},
	}
</script>
<style scoped></style>
