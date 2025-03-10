export const createColumnChartConfig = ({
	series,
	labels,
	logBase,
	enableLogarithmic,
	yStartValue,
	tickAmount,
}) => {
	return {
		series: [
			{
				name: 'Количество',
				data: series,
			},
		],
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
				id: 'column',
				type: 'bar',
				background: '#fff',
				redrawOnParentResize: false,
				zoom: {
					enabled: false,
				},
				toolbar: {
					show: false,
				},
			},
			plotOptions: {
				bar: {
					borderRadius: 5,
					columnWidth: '85%',
					dataLabels: {
						position: 'top', // top, center, bottom
					},
					// distributed: true,
					columnWidth: '90%',
					barHeight: '50%',
					distributed: false,
					hideZeroBarsWhenGrouped: false,
					isDumbbell: false,
					dumbbellColors: undefined,
					isFunnel: false,
					isFunnel3d: false,
					colors: {
						ranges: [
							{
								from: 0,
								to: 0,
								color: undefined,
							},
						],
						backgroundBarColors: [],
						backgroundBarOpacity: 1,
						backgroundBarRadius: 0,
					},
				},
			},

			dataLabels: {
				enabled: true,
				formatter: function (val) {
					function numberWithCommas(x) {
						return x
							.toString()
							.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
					}
					return numberWithCommas(val)
				},
				offsetY: -20,
				style: {
					fontSize: '10px',
					colors: ['#304758'],
				},
			},

			xaxis: {
				categories: labels,
				tickAmount: 30,
				position: 'bottom',

				labels: {
					show: true,
					hideOverlappingLabels: true,
					trim: true,
					style: {
						fontSize: 12,
					},
				},
				crosshairs: {
					fill: {
						type: 'gradient',
						gradient: {
							colorFrom: '#D8E3F0',
							colorTo: '#BED1E6',
							stops: [0, 100],
							opacityFrom: 0.4,
							opacityTo: 0.5,
						},
					},
				},
				tooltip: {
					enabled: false,
				},
			},
			yaxis: {
				show: true,
				showAlways: false,
				showForNullSeries: true,
				seriesName: undefined,
				opposite: false,
				reversed: false,
				logarithmic: enableLogarithmic,
				logBase: logBase,
				tickAmount: tickAmount,
				min: yStartValue,
				max: undefined,
				stepSize: undefined,
				forceNiceScale: true,
				floating: false,
				decimalsInFloat: undefined,
				labels: {
					show: true,
					showDuplicates: false,
					align: 'left',
					minWidth: 0,
					maxWidth: undefined,
					style: {
						colors: [],
						fontSize: '12px',
						fontWeight: 400,
						cssClass: 'apexcharts-yaxis-label',
					},
					offsetX: 0,
					offsetY: 0,
					rotate: 0,
					formatter: function (val, index) {
						function numberWithCommas(x) {
							return x
								.toString()
								.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
						}
						return numberWithCommas(val.toFixed(0))
					},
				},
				axisBorder: {
					show: false,
				},

				axisTicks: {
					show: true,
					borderType: 'solid',
					// color: '#78909C',
					width: 10,
					offsetX: 0,
					offsetY: 0,
				},

				tooltip: {
					enabled: false,
					offsetX: 0,
				},
			},
			legend: {
				show: false,
			},
			grid: {
				show: true,
				borderColor: '#e0e0e0',
				xaxis: {
					lines: {
						show: true,
					},
				},
				yaxis: {
					lines: {
						show: true,
					},
				},
				row: {
					opacity: 0.5,
				},
				column: {
					opacity: 0.5,
				},

				padding: {
					top: -20,
					bottom: 0,
					right: 0,
					left: 15,
				},
			},

			fill: {
				type: 'gradient',
				gradient: {
					shade: 'light',
					type: 'horizontal',
					shadeIntensity: 0.25,
					gradientToColors: undefined,
					inverseColors: true,
					opacityFrom: 0.85,
					opacityTo: 0.85,
					stops: [50, 0, 100],
				},
			},
			noData: {
				text: 'Нет данных',
			},
			tooltip: {
				enabled: true,
				enabledOnSeries: undefined,
				shared: true,
				followCursor: false,
				intersect: false,
				inverseOrder: false,
				// custom: function ({
				// 	series,
				// 	seriesIndex,
				// 	dataPointIndex,
				// 	w,
				// }) {
				// 	console.log(
				// 		w.globals.labels[dataPointIndex],
				// 		series,
				// 		dataPointIndex,
				// 	)
				// 	function numberWithCommas(x) {
				// 		return x
				// 			.toString()
				// 			.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
				// 	}
				// 	// Создание элемента
				// 	const customElement = document.createElement('div')
				// 	customElement.className = 'custom-tooltip'
				// 	customElement.innerHTML = `
				// 		${w.globals.labels[dataPointIndex]}:
				// 		<span class="custom-tooltip__count">${numberWithCommas(series[seriesIndex][dataPointIndex])}</span>
				// 	`
				// 	return customElement
				// },
				hideEmptySeries: true,
				fillSeriesColor: false,
				theme: 'light',
				style: {
					fontSize: '12px',
					fontFamily: undefined,
				},
				onDatasetHover: {
					highlightDataSeries: true,
				},
				x: {
					show: true,
					format: 'dd MMM',
					formatter: undefined,
				},
				y: {
					formatter: function (
						value,
						{ series, seriesIndex, dataPointIndex, w },
					) {
						function numberWithCommas(x) {
							return x
								.toString()
								.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
						}
						return numberWithCommas(value)
					},
				},
				// y: {
				// 	formatter: undefined,
				// 	title: {
				// 		formatter: function (val) {
				// 			function numberWithCommas(x) {
				// 				return x
				// 					.toString()
				// 					.replace(
				// 						/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g,
				// 						',',
				// 					)
				// 			}
				// 			return numberWithCommas(val)
				// 		},
				// 	},
				// },

				marker: {
					show: true,
				},

				fixed: {
					enabled: false,
					position: 'topRight',
					offsetX: 0,
					offsetY: 0,
				},
			},
			responsive: [
				{
					breakpoint: 800,
					options: {
						dataLabels: {
							enabled: false,
						},
						yaxis: {
							show: false,
							logarithmic: enableLogarithmic,
							logBase: logBase,
							tickAmount: tickAmount,
							min: yStartValue,
						},
						xaxis: {
							labels: {
								show: true,
							},
						},
					},
				},
			],
		},
	}
}
