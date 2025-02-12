export const createHorizontalBarChartConfig = ({ series, labels }) => {
	const data = series.map((item, index) => {
		return {
			y: labels[index],
			x: item,
		}
	})
	console.log(data)
	return {
		series: [{ name: 'Документов', data: series }],
		chartOptions: {
			chart: {
				animations: {
					enabled: true,
				},
				background: '#fff',
				height: '100%',
				id: 'Колличество_нормативных_правовых_актов_в_каждомокруге',
				stacked: true,
				toolbar: {
					show: true,
				},
				type: 'bar',
				width: '100%',
			},
			plotOptions: {
				xaxis: {
					categories: labels,
				},

				bar: {
					horizontal: true,
					borderRadius: 10,
					borderRadiusApplication: 'end',
					borderRadiusWhenStacked: 'last',
					// hideZeroBarsWhenGrouped: false,
					isDumbbell: false,
					isFunnel: false,
					isFunnel3d: true,
					dataLabels: {
						total: {
							enabled: true,
							offsetX: -50,
							offsetY: 0,
							style: {
								color: '#ffffff',
								fontSize: '12px',
								fontWeight: 600,
							},
						},
					},
				},
			},
			dataLabels: {
				enabled: false,
			},
			fill: {
				opacity: 1,
			},
			grid: {
				padding: {
					right: 25,
					left: 15,
				},
			},
			legend: {
				enabled: true,
				fontSize: 14,
				offsetY: 0,
				clusterGroupedSeries: true,
				clusterGroupedSeriesOrientation: 'vertical',
				markers: {
					size: 7,
					shape: 'square',
				},
				itemMargin: {
					vertical: 0,
				},
			},
			markers: {},

			states: {
				hover: {
					filter: {},
				},
				active: {
					filter: {},
				},
			},
			stroke: {
				width: 1,
				fill: {
					type: 'solid',
					opacity: 0.85,
					gradient: {
						shade: 'dark',
						type: 'horizontal',
						shadeIntensity: 0.5,
						inverseColors: true,
						opacityFrom: 1,
						opacityTo: 1,
						stops: [0, 50, 100],
						colorStops: [],
					},
				},
			},
			tooltip: {
				shared: false,
				hideEmptySeries: false,
				intersect: true,
			},
			xaxis: {
				categories: labels,
				labels: {
					trim: true,
					style: {},
				},
				group: {
					groups: [],
					style: {
						colors: [],
						fontSize: '12px',
						fontWeight: 400,
						cssClass: '',
					},
				},
				tickPlacement: 'between',
				title: {
					style: {
						fontWeight: 700,
					},
				},
				tooltip: {
					enabled: false,
				},
			},
		},
	}
}
