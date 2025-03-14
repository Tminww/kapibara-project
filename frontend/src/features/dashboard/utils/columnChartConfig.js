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
				},
				id: 'column',
				type: 'bar',
				background: '#fff',
				redrawOnParentResize: true,
				zoom: {
					enabled: false,
				},
				toolbar: {
					show: false,
				},
			},
			plotOptions: {
				bar: {
					horizontal: false, // По умолчанию вертикальный
					borderRadius: 5,
					columnWidth: '90%',
					dataLabels: {
						position: 'top',
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
				offsetY: -15,
				style: {
					fontSize: '10px',
					colors: ['#304758'],
				},
			},
			xaxis: {
				categories: labels,
				tickAmount: tickAmount || labels.length,
				position: 'bottom',
				labels: {
					show: true,
					hideOverlappingLabels: true,
					trim: true,
					rotate: -30,
					rotateAlways: false,
					style: {
						fontSize: '10px',
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
				logarithmic: enableLogarithmic,
				logBase: logBase,
				tickAmount: tickAmount,
				min: yStartValue,
				labels: {
					show: true,
					align: 'left',
					style: {
						fontSize: '10px',
						fontWeight: 400,
					},
					formatter: function (val) {
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
					width: 6,
				},
			},
			legend: {
				show: false,
			},
			grid: {
				show: true,
				borderColor: '#e0e0e0',
				padding: {
					top: -15,
					bottom: -5,
					right: 0,
					left: 10,
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
				followCursor: false,
				y: {
					formatter: function (value) {
						function numberWithCommas(x) {
							return x
								.toString()
								.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
						}
						return numberWithCommas(value)
					},
				},
			},
			responsive: [
				{
					breakpoint: 400,
					options: {
						dataLabels: {
							enabled: false,
						},
						yaxis: {
							show: true,
						},
						xaxis: {
							labels: {
								show: true,
								hideOverlappingLabels: true,
								trim: false,
								rotate: -30,
								rotateAlways: false,
								style: {
									fontSize: '12px',
								},
							},
						},
					},
				},
			],
		},
	}
}
