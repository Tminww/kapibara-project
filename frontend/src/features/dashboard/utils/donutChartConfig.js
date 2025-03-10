import { he } from 'vuetify/lib/locale/index.mjs'

export const createDonutChartConfig = ({
	series,
	labels,
	isLegendClickable,
	legendPosition,
	router,
}) => {
	return {
		series: series,
		chartOptions: {
			chart: {
				animations: {
					enabled: false,
					speed: 1000,
					animateGradually: {
						enabled: true,
						delay: 1000,
					},
					dynamicAnimation: {
						enabled: true,
						speed: 1000,
					},
				},

				background: '#fff',

				id: 'Колличество_нормативных_правовых_актов_в_каждом_округе',
				type: 'donut',
				toolbar: {
					show: false,
					offsetX: 0,
					offsetY: 0,
					tools: {
						download: true,
						selection: false,
						zoom: true,
						zoomin: true,
						zoomout: true,
						pan: true,
					},
					customIcons: [],

					autoSelected: 'zoom',
				},
				events: {
					legendClick: (chart, seriesIndex, config) => {
						console.log('Clicked legend item', seriesIndex)
						// Используем Vue Router
						const label = config.globals.labels[seriesIndex]
						if (isLegendClickable) {
							router.push({ name: 'district', params: { label } }) // или другой маршрут
						}
					},
				},
			},

			plotOptions: {
				pie: {
					donut: {
						size: '65%',
						background: 'transparent',
						labels: {
							show: true,
							name: {
								show: true,
								fontSize: '10px',
								fontWeight: 600,
								color: '#000',
								offsetY: 0,
								formatter: function (val) {
									return val
								},
							},
							value: {
								show: true,
								fontSize: '16px',
								fontWeight: 400,
								color: undefined,
								offsetY: 16,
								formatter: function (val) {
									function numberWithCommas(x) {
										return x
											.toString()
											.replace(
												/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g,
												'.',
											)
									}
									return numberWithCommas(val)
								},
							},
							total: {
								show: true,
								showAlways: false,
								label: 'ВСЕГО',
								fontSize: '14px',
								fontWeight: 600,
								color: '#373d3f',
								formatter: function (val) {
									function numberWithCommas(x) {
										return x
											.toString()
											.replace(
												/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g,
												'.',
											)
									}
									return numberWithCommas(val)
								},
								formatter: function (w) {
									function numberWithCommas(x) {
										return x
											.toString()
											.replace(
												/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g,
												'.',
											)
									}
									return numberWithCommas(
										w.globals.seriesTotals.reduce(
											(a, b) => {
												return a + b
											},
											0,
										),
									)
								},
							},
						},
					},
				},
			},
			labels: labels,
			dataLabels: {
				enabled: true,
				enabledOnSeries: undefined,
				textAnchor: 'middle',
				distributed: false,
				offsetX: 0,
				offsetY: 0,
				style: {
					fontSize: '12px',
					fontFamily: 'Helvetica, Arial, sans-serif',
					fontWeight: 'bold',
					colors: ['#000'],
				},
				background: {
					enabled: false,
					foreColor: '#fff',
					padding: 4,
					borderRadius: 2,
					borderWidth: 1,
					borderColor: '#fff',
					opacity: 0.9,
					dropShadow: {
						enabled: false,
						top: 1,
						left: 1,
						blur: 1,
						color: '#000',
						opacity: 0.45,
					},
				},
				dropShadow: {
					enabled: false,
					top: 1,
					left: 1,
					blur: 1,
					color: '#fff',
					opacity: 1,
				},
			},
			legend: {
				show: true,
				showForSingleSeries: false,
				showForNullSeries: true,
				showForZeroSeries: true,
				position: legendPosition,
				horizontalAlign: 'center',
				floating: false,
				fontSize: '14px',
				fontWeight: 400,
				formatter: (seriesName, opts) => {
					function numberWithCommas(x) {
						return x
							.toString()
							.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
					}
					return `${seriesName}: ${numberWithCommas(opts.w.globals.series[opts.seriesIndex])}`
				},
				inverseOrder: false,
				tooltipHoverFormatter: undefined,
				customLegendItems: [],
				clusterGroupedSeries: true,
				clusterGroupedSeriesOrientation: 'vertical',
				offsetX: 0,
				offsetY: 0,
				labels: {
					hideOverlappingLabels: true,
					trim: true,
					colors: undefined,
					useSeriesColors: false,
				},
				markers: {
					size: 7,
					shape: undefined,
					strokeWidth: 1,
					fillColors: undefined,
					customHTML: undefined,
					onClick: undefined,
					offsetX: 0,
					offsetY: 0,
				},
				itemMargin: {
					horizontal: 5,
					vertical: 6,
				},
			},
			noData: {
				text: 'Нет данных',
				style: {
					color: undefined,
					fontSize: '20px',
					fontFamily: 'Nunito',
				},
			},

			fill: {
				type: 'pattern',
				opacity: 1,
				pattern: {
					enabled: true,
					style: [],
				},
			},
			states: {
				hover: {
					filter: 'none',
				},
			},
			theme: {
				palette: 'palette7',
				monochrome: {
					enabled: true,
					color: '#2196F3',
					shadeTo: 'light',
					shadeIntensity: 0.65,
				},
			},
			title: {
				text: '',
			},

			tooltip: {
				enabled: false,

				hideEmptySeries: true,
				fillSeriesColor: false,
				theme: false,
				style: {
					fontSize: '12px',
					fontFamily: undefined,
				},
				onDatasetHover: {
					highlightDataSeries: false,
				},
				x: {
					show: true,
					format: 'dd MMM',
					formatter: undefined,
				},
				y: {
					formatter: undefined,
					title: {
						formatter: seriesName => seriesName,
					},
				},
				z: {
					formatter: undefined,
					title: 'Size: ',
				},
				marker: {
					show: true,
				},

				fixed: {
					enabled: true,
					position: 'topRight',
					offsetX: 0,
					offsetY: 0,
				},
			},
			// responsive: [
			// 	{
			// 		breakpoint: 800,
			// 		options: {
			// 			dataLabels: {
			// 				enabled: true,
			// 			},
			// 			legend: {
			// 				show: true,
			// 				position: 'bottom',
			// 				height: 100,
			// 			},
			// 		},
			// 	},
			// ],
		},
	}
}
