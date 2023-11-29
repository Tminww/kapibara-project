<template>
    <v-card class="rounded-xl mx-auto" elevation="0" variant="outlined" width="500">
        <v-card-title class="text-h6 mb-1">
            {{ name }}
        </v-card-title>

        <v-card-subtitle class="text-h6 mb-1">
            {{ count }}
        </v-card-subtitle>

        <v-card-text>
            <doughnut-chart v-if="loaded" :chart-data="this.chartData" :chart-options="this.chartOptions" />
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
            name: this.all.name,
            count: this.all.count,
            stat: this.all.stat,
            chartData: {
                labels: [],
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

                        data: []
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                layout: {
                    padding: {
                        left: 0,
                        right: 0,
                    }
                },
                plugins: {
                    legend: {
                        position: 'right',
                        display: true,
                        labels: {
                            // fullSize: true,
                            labels: [],


                            font: {
                                size: 14,
                                family: 'Helvetica',
                                style: 'bold',
                            }
                        }
                    }


                }
            },
        }
    },

    methods: {
        setup() {
            let labels = []
            let data = []
            for (const row of this.stat) {
                labels.push(row.name)
                data.push(row.count)
            }
            this.chartData.labels = labels
            this.chartData.datasets[0].data = data
        },
    },
    async mounted() {
        this.loaded = false
        this.setup()
        this.loaded = true
    },
}
</script>

<style scoped></style>
