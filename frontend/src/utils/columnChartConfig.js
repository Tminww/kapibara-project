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
					enabled: true,
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
				width: '100%',
				background: '#fff',
				height: 150,
				redrawOnParentResize: false,
				zoom: {
					enabled: false,
					type: 'x',
					autoScaleYaxis: true,
					allowMouseWheelZoom: false,
					zoomedArea: {
						fill: {
							color: '#90CAF9',
							opacity: 0.4,
						},
						stroke: {
							color: '#0D47A1',
							opacity: 0.4,
							width: 1,
						},
					},
				},
			},
			plotOptions: {
				bar: {
					borderRadius: 10,
					columnWidth: '85%',
					barHeight: '10%', // Столбцы станут ниже
					dataLabels: {
						position: 'top', // top, center, bottom
					},
					// distributed: true,
					borderRadiusApplication: 'around',
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
					return val
				},
				offsetY: -20,
				style: {
					fontSize: '10px',
					colors: ['#304758'],
				},
			},
			stroke: {
				width: 0,
			},

			xaxis: {
				categories: labels,
				tickAmount: 30,
				position: 'bottom',
				axisBorder: {
					show: false,
				},
				axisTicks: {
					show: true,
				},
				labels: {
					show: true,
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
						return val.toFixed(0)
					},
				},
				axisBorder: {
					show: true,
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
					top: 10,
					bottom: 0,
					right: 0,
					left: 14,
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
		},
	}
}
