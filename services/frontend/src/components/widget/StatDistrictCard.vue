<template>
    <v-card class="rounded-xl mx-auto" elevation="8" width="500">
        <v-toolbar dense flat class="text-h6 mb-1 px-4" color="primary lighten-2">{{ name }}
        </v-toolbar>
        <v-card-title class="text-h6 mb-1">
            {{ count }}
        </v-card-title>

        <!-- <v-card-title class="text-h6 mb-1">
            {{ name }}
        </v-card-title>

        <v-card-subtitle class="text-h6 mb-1">
            {{ count }}
        </v-card-subtitle> -->

        <v-card-text>
            <div class="justify-center">
                <doughnut-chart v-if="loaded" :chart-data="this.chartData" :chart-options="this.chartOptions" />
            </div>
        </v-card-text>

        <v-card-actions class="justify-center">
            <v-btn> Открыть статистику </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="js">
import DoughnutChart from './DoughnutChart.vue'
export default {
    name: 'stat-district-card',

    components: { DoughnutChart },
    props: {
        district: { type: Object, required: true },
    },

    data() {
        return {
            loaded: false,
            name: this.district.name,
            count: this.district.count,
            stat: this.district.stat,

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

                        data: [],
                    },
                ],
            },
            chartOptions: {
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
