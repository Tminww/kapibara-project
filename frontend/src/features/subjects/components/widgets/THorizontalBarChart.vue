<template>
    <apexchart :options="data.chartOptions" :series="data.series" :height="height"></apexchart>
</template>

<script setup lang="js">
import { computed } from 'vue'

const props = defineProps({
    labels: { type: Array, required: true },
    series: { type: Array, required: true },
    height: { type: Number, required: false },
    logBase: { type: Number, default: 10 },
    enableLogarithmic: { type: Boolean, default: true },
    yStartValue: { type: Number, default: 0.5 },
    tickAmount: { type: Number, default: undefined }
})

const data = computed(() => {
    return {
        series: [
            {
                name: 'Количество',
                data: props.series
            }
        ],
        chartOptions: {
            chart: {
                animations: {
                    enabled: false,
                    speed: 1000,
                    animateGradually: {
                        enabled: true,
                        delay: 1000
                    },
                    dynamicAnimation: {
                        enabled: true,
                        speed: 1000
                    }
                },
                id: 'column',
                type: 'bar',
                background: '#fff',
                redrawOnParentResize: false,
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    horizontal: true,
                    dataLabels: {
                        position: 'top' // top, center, bottom
                    },
                    // distributed: true,
                    borderRadiusApplication: 'around',
                    columnWidth: '90%',
                    barHeight: '90%',
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
                                color: undefined
                            }
                        ],
                        backgroundBarColors: [],
                        backgroundBarOpacity: 1,
                        backgroundBarRadius: 0
                    }
                }
            },

            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    function numberWithCommas(x) {
                        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
                    }
                    return numberWithCommas(val)
                },
                offsetX: -20,
                style: {
                    fontSize: '12px',
                    colors: ['#304758']
                }
            },
            stroke: {
                width: 0
            },

            xaxis: {
                categories: props.labels,
                tickAmount: 10,
                position: 'bottom',
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: true
                },

                tooltip: {
                    enabled: false
                }
            },
            yaxis: {
                show: true,
                showAlways: false,
                showForNullSeries: true,
                seriesName: undefined,
                opposite: false,
                reversed: false,

                logarithmic: props.enableLogarithmic,
                logBase: props.logBase,
                tickAmount: props.tickAmount,
                min: props.yStartValue,
                max: undefined,
                stepSize: undefined,
                forceNiceScale: true,
                floating: false,
                decimalsInFloat: undefined,
                labels: {
                    show: true,
                    showDuplicates: false,

                    style: {
                        colors: [],
                        fontSize: '12px',
                        fontWeight: 400,
                        cssClass: 'apexcharts-yaxis-label'
                    },
                    offsetX: 0,
                    offsetY: 0,
                    rotate: 0,
                    formatter: function (val, index) {
                        return val
                    }
                },
                axisBorder: {
                    show: true
                },

                axisTicks: {
                    show: true,
                    borderType: 'solid',
                    // color: '#78909C',
                    offsetX: 0,
                    offsetY: 0
                },

                tooltip: {
                    enabled: false,
                    offsetX: 0
                }
            },
            legend: {
                show: false
            },
            grid: {
                show: true,
                borderColor: '#e0e0e0',
                xaxis: {
                    lines: {
                        show: true
                    }
                },
                yaxis: {
                    lines: {
                        show: true
                    }
                },
                row: {
                    opacity: 0.5
                },
                column: {
                    opacity: 0.5
                },

                padding: {
                    top: -20,
                    bottom: 0,
                    right: 0,
                    left: 0
                }
            },

            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: 'vertical',
                    shadeIntensity: 0.25,
                    gradientToColors: undefined,
                    inverseColors: true,
                    opacityFrom: 0.85,
                    opacityTo: 0.85,
                    stops: [50, 0, 100]
                }
            },
            tooltip: {
                // custom: function ({ series, seriesIndex, dataPointIndex, w }) {
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
                y: {
                    formatter: function (value, { series, seriesIndex, dataPointIndex, w }) {
                        function numberWithCommas(x) {
                            return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
                        }
                        return numberWithCommas(value)
                    }
                }
            }
            // responsive: [
            // 	{
            // 		breakpoint: 800,
            // 		options: {
            // 			dataLabels: {
            // 				enabled: true,
            // 			},
            // 			yaxis: {
            // 				show: true,
            // 				logarithmic: enableLogarithmic,
            // 				logBase: logBase,
            // 				tickAmount: tickAmount,
            // 				min: yStartValue,
            // 			},
            // 			xaxis: {
            // 				labels: {
            // 					show: false,
            // 				},
            // 			},
            // 		},
            // 	},
            // ],
        }
    }
})
</script>
