<template>
    <Doughnut id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>
  
<script lang="js">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale)

export default {
    name: 'doughnut-chart',
    components: { Doughnut },
    props: {
        chartData: {
            type: Object,
            required: true
        },
        chartOptions: {
            type: Object,
            default: () => { }
        }
    },
}
</script>
  