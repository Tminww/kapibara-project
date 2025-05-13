<template>
    <apexchart
        :options="data.chartOptions"
        :series="data.series"
        :height="props.height"
    ></apexchart>
</template>

<script setup lang="js">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
    labels: { type: Array, required: true },
    series: { type: Array, required: true },
    height: { type: Number, required: false },
    legendPosition: {
        type: String,
        default: 'left',
        validators: ['top', 'bottom', 'left', 'right']
    },
    isLegendClickable: { type: Boolean, default: false },
    routeName: { type: String, default: 'region' }
})

const router = useRouter()

const mapNameToId = {
    'Центральный ФО': 1,
    'Северо-Западный ФО': 2,
    'Южный ФО': 3,
    'Приволжский ФО': 4,
    'Уральский ФО': 5,
    'Сибирский ФО': 6,
    'Дальневосточный ФО': 7,
    'Северо-Кавказский ФО': 8
}

const getDistrictIdByName = (name) => {
    return mapNameToId[name]
}

const data = computed(() => {
    return {
        series: props.series,
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
                        pan: true
                    },
                    customIcons: [],

                    autoSelected: 'zoom'
                },
                events: {
                    legendClick: (chart, seriesIndex, config) => {
                        // Используем Vue Router
                        const label = config.globals.labels[seriesIndex]
                        if (props.isLegendClickable) {
                            router.push({
                                name: props.routeName,
                                params: { id: getDistrictIdByName(label) },
                                query: { label: label }
                            }) // или другой маршрут
                        }
                    }
                }
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
                                }
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
                                            .replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
                                    }
                                    return numberWithCommas(val)
                                }
                            },
                            total: {
                                show: true,
                                showAlways: false,
                                label: 'ВСЕГО',
                                fontSize: '14px',
                                fontWeight: 600,
                                color: '#373d3f',
                                // formatter: function (val) {
                                //     function numberWithCommas(x) {
                                //         return x
                                //             .toString()
                                //             .replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
                                //     }
                                //     return numberWithCommas(val)
                                // },
                                formatter: function (w) {
                                    function numberWithCommas(x) {
                                        return x
                                            .toString()
                                            .replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
                                    }
                                    return numberWithCommas(
                                        w.globals.seriesTotals.reduce((a, b) => {
                                            return a + b
                                        }, 0)
                                    )
                                }
                            }
                        }
                    }
                }
            },
            labels: props.labels,
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
                    colors: ['#000']
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
                        opacity: 0.45
                    }
                },
                dropShadow: {
                    enabled: false,
                    top: 1,
                    left: 1,
                    blur: 1,
                    color: '#fff',
                    opacity: 1
                }
            },
            legend: {
                show: true,
                showForSingleSeries: false,
                showForNullSeries: true,
                showForZeroSeries: true,
                position: props.legendPosition,
                horizontalAlign: 'center',
                floating: false,
                fontSize: '14px',
                fontWeight: 400,
                formatter: (seriesName, opts) => {
                    function numberWithCommas(x) {
                        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.')
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

                itemMargin: { horizontal: 7, vertical: 5 },
                height: 80, // Позволяет легенде адаптироваться по высоте
                width: 'auto', // Позволяет легенде адаптироваться по ширине
                labels: {
                    hideOverlappingLabels: false, // Убеждаемся, что метки не скрываются
                    trim: false
                }
                // customHTML: function (seriesName, opts) {
                // 	const value = opts.w.globals.series[opts.seriesIndex] || 0
                // 	return `
                // 	  <div class="legend-item" style="display: flex; align-items: center; padding: 2px 0;">
                // 		<span style="display: inline-block; width: 10px; height: 10px; background-color: ${opts.w.config.colors[opts.seriesIndex % opts.w.config.colors.length]}; margin-right: 5px;"></span>
                // 		<span>${seriesName}: ${value.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, '.') || '0'}</span>
                // 	  </div>
                // 	`
                // },
            },
            noData: {
                text: 'Нет данных',
                style: {
                    color: undefined,
                    fontSize: '20px',
                    fontFamily: 'Nunito'
                }
            },

            fill: {
                type: 'pattern',
                opacity: 1,
                pattern: {
                    enabled: true,
                    style: []
                }
            },
            states: {
                hover: {
                    filter: 'none'
                }
            },
            theme: {
                palette: 'palette7',
                monochrome: {
                    enabled: true,
                    color: '#2196F3',
                    shadeTo: 'light',
                    shadeIntensity: 0.65
                }
            },
            title: {
                text: ''
            },

            tooltip: {
                enabled: false,

                hideEmptySeries: true,
                fillSeriesColor: false,
                theme: false,
                style: {
                    fontSize: '12px',
                    fontFamily: undefined
                },
                onDatasetHover: {
                    highlightDataSeries: false
                },
                x: {
                    show: true,
                    format: 'dd MMM',
                    formatter: undefined
                },
                y: {
                    formatter: undefined,
                    title: {
                        formatter: (seriesName) => seriesName
                    }
                },
                z: {
                    formatter: undefined,
                    title: 'Size: '
                },
                marker: {
                    show: true
                },

                fixed: {
                    enabled: true,
                    position: 'topRight',
                    offsetX: 0,
                    offsetY: 0
                }
            }
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
        }
    }
})
</script>
