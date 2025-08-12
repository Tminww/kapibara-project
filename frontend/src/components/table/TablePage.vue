<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref } from 'vue'

const route = useRoute()
const router = useRouter()
const tableData = ref([])

const productId = computed(() => route.params.id)
const productName = computed(() => route.query.name)
const productValue = computed(() => route.query.value)

// Симуляция загрузки данных на основе ID
const loadTableData = (id) => {
  // Здесь вы можете загрузить данные с сервера по ID
  const mockData = {
    product_1: [
      { period: 'Январь', value: 12, percent: 27.3, status: 'Активно' },
      { period: 'Февраль', value: 15, percent: 34.1, status: 'Активно' },
      { period: 'Март', value: 17, percent: 38.6, status: 'Завершено' }
    ],
    product_2: [
      { period: 'Январь', value: 18, percent: 32.7, status: 'Активно' },
      { period: 'Февраль', value: 20, percent: 36.4, status: 'Активно' },
      { period: 'Март', value: 17, percent: 30.9, status: 'Приостановлено' }
    ],
    product_3: [
      { period: 'Январь', value: 14, percent: 34.1, status: 'Активно' },
      { period: 'Февраль', value: 13, percent: 31.7, status: 'Активно' },
      { period: 'Март', value: 14, percent: 34.1, status: 'Активно' }
    ],
    product_4: [
      { period: 'Январь', value: 22, percent: 32.8, status: 'Активно' },
      { period: 'Февраль', value: 23, percent: 34.3, status: 'Активно' },
      { period: 'Март', value: 22, percent: 32.8, status: 'Завершено' }
    ],
    product_5: [
      { period: 'Январь', value: 8, percent: 36.4, status: 'Приостановлено' },
      { period: 'Февраль', value: 7, percent: 31.8, status: 'Приостановлено' },
      { period: 'Март', value: 7, percent: 31.8, status: 'Активно' }
    ]
  }

  return mockData[id] || []
}

const goBack = () => {
  router.go(-1) // или router.push('/chart')
}

onMounted(() => {
  tableData.value = loadTableData(productId.value)
})
</script>

<template>
  <div>
    {{}}
    <h2>Детальная таблица для: {{ productName }}</h2>

    <div class="product-info">
      <p><strong>ID:</strong> {{ productId }}</p>
      <p><strong>Название:</strong> {{ productName }}</p>
      <p><strong>Значение:</strong> {{ productValue }}</p>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Период</th>
          <th>Значение</th>
          <th>Процент</th>
          <th>Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in tableData" :key="row.period">
          <td>{{ row.period }}</td>
          <td>{{ row.value }}</td>
          <td>{{ row.percent }}%</td>
          <td>{{ row.status }}</td>
        </tr>
      </tbody>
    </table>

    <button @click="goBack" class="back-button">← Назад к графику</button>
  </div>
</template>

<style scoped>
.product-info {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.data-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.back-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.back-button:hover {
  background-color: #0056b3;
}
</style>
