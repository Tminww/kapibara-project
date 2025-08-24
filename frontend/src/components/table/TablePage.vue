<template>
  <v-container>
    <!-- Информационная карточка -->
    <!-- Кнопка возврата -->
    <div class="d-flex justify-start mb-6">
      <v-btn
        prepend-icon="mdi-arrow-left"
        color="primary"
        variant="outlined"
        size="large"
        @click="goBack"
      >
        Назад к графикам
      </v-btn>
    </div>
    <v-card class="mb-6" elevation="2">
      <v-card-title class="bg-primary text-white">
        <v-icon icon="mdi-table" class="me-2"></v-icon>
        Детальная таблица документов
      </v-card-title>

      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="3">
            <v-chip color="primary" variant="outlined" size="large">
              <v-icon icon="mdi-filter" start></v-icon>
              {{ filterTypeLabel }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="3">
            <v-chip color="secondary" variant="outlined" size="large">
              <v-icon icon="mdi-magnify" start></v-icon>
              {{ filterLabel }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="3" v-if="filterName">
            <v-chip color="accent" variant="outlined" size="large">
              <v-icon icon="mdi-map-marker" start></v-icon>
              {{ filterName }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="3" v-if="dateRange">
            <v-chip color="warning" variant="outlined" size="large">
              <v-icon icon="mdi-calendar-range" start></v-icon>
              {{ dateRange }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="3" class="mt-2">
            <v-chip color="info" size="large">
              <v-icon icon="mdi-file-document-multiple" start></v-icon>
              Всего: {{ totalDocuments }} документов
            </v-chip>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Панель управления таблицей -->
    <!-- <v-card class="mb-4">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="3">
            <v-select
              v-model="itemsPerPage"
              :items="[10, 20, 50, 100]"
              label="Записей на странице"
              density="compact"
              variant="outlined"
              @update:model-value="loadDocuments"
            ></v-select>
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              item-title="text"
              item-value="value"
              label="Сортировать по"
              density="compact"
              variant="outlined"
              @update:model-value="loadDocuments"
            ></v-select>
          </v-col>

          <v-col cols="12" md="2">
            <v-btn-toggle
              v-model="sortOrder"
              mandatory
              density="compact"
              @update:model-value="loadDocuments"
            >
              <v-btn value="desc" icon="mdi-sort-descending"></v-btn>
              <v-btn value="asc" icon="mdi-sort-ascending"></v-btn>
            </v-btn-toggle>
          </v-col>

          <v-col cols="12" md="4" class="d-flex justify-end"> </v-col>
        </v-row>
      </v-card-text>
    </v-card> -->

    <!-- Таблица документов -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="documents"
        :loading="loading"
        :items-per-page="itemsPerPage"
        :page="currentPage"
        hide-default-footer
        class="elevation-1"
      >
        <!-- Колонка с номером документа -->
        <template v-slot:item.eo_number="{ item }">
          <v-chip v-if="item.eo_number" color="primary" variant="outlined" size="small">
            {{ item.eo_number }}
          </v-chip>
          <span v-else class="text-grey">—</span>
        </template>

        <!-- Колонка с названием -->
        <template v-slot:item.name="{ item }">
          <div style="max-width: 300px">
            <v-tooltip :text="item.name || item.title">
              <template v-slot:activator="{ props }">
                <span v-bind="props" class="text-truncate d-block">
                  {{ item.name || item.title || '—' }}
                </span>
              </template>
            </v-tooltip>
          </div>
        </template>

        <!-- Колонка с типом документа -->
        <template v-slot:item.type_name="{ item }">
          <v-chip color="secondary" variant="tonal" size="small">
            {{ item.type_name || '—' }}
          </v-chip>
        </template>

        <!-- Колонка с регионом -->
        <template v-slot:item.region_name="{ item }">
          <div class="d-flex flex-column">
            <span class="font-weight-medium">{{ item.region_name || '—' }}</span>
            <span v-if="item.district_name" class="text-caption text-grey">
              {{ item.district_name }}
            </span>
          </div>
        </template>

        <!-- Колонка с датами -->
        <template v-slot:item.dates="{ item }">
          <div class="d-flex flex-column">
            <div v-if="item.date_of_publication">
              <v-icon size="small" color="success">mdi-calendar-check</v-icon>
              <span class="text-caption ml-1">
                {{ formatDate(item.date_of_publication) }}
              </span>
            </div>
            <div v-if="item.date_of_signing">
              <v-icon size="small" color="info">mdi-pen</v-icon>
              <span class="text-caption ml-1">
                {{ formatDate(item.date_of_signing) }}
              </span>
            </div>
          </div>
        </template>

        <!-- Колонка с количеством страниц -->
        <template v-slot:item.pages_count="{ item }">
          <v-chip v-if="item.pages_count" color="info" variant="outlined" size="small">
            <v-icon start size="small">mdi-file-document</v-icon>
            {{ item.pages_count }}
          </v-chip>
          <span v-else class="text-grey">—</span>
        </template>

        <!-- Колонка с действиями -->
        <template v-slot:item.actions="{ item }">
          <v-btn
            v-if="item.eo_number"
            color="primary"
            variant="tonal"
            size="small"
            :href="urlPravoGovRuPath + item.eo_number"
            target="_blank"
            class="text-none"
          >
            <v-icon start size="small">mdi-open-in-new</v-icon>
            Открыть
          </v-btn>
          <v-tooltip v-else text="Номер документа отсутствует">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                color="grey"
                variant="tonal"
                size="small"
                disabled
                class="text-none"
              >
                <v-icon start size="small">mdi-open-in-new</v-icon>
                Открыть
              </v-btn>
            </template>
          </v-tooltip>
        </template>

        <!-- Загрузка -->
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
        </template>

        <!-- Пустое состояние -->
        <template v-slot:no-data>
          <div class="text-center py-8">
            <v-icon size="64" color="grey-lighten-2">mdi-file-document-remove</v-icon>
            <div class="text-h6 text-grey mt-4">Документы не найдены</div>
            <div class="text-body-2 text-grey">Попробуйте изменить параметры фильтрации</div>
          </div>
        </template>
      </v-data-table>

      <!-- Пагинация -->
      <v-divider></v-divider>
      <div class="d-flex justify-center pa-4">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="7"
          @update:model-value="loadDocuments"
        ></v-pagination>
      </div>
    </v-card>

    <!-- Снекбар для ошибок -->
    <v-snackbar v-model="errorSnackbar" color="error" timeout="5000" location="top right">
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="errorSnackbar = false"> Закрыть </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import api from '@/api'

const route = useRoute()
const router = useRouter()

// Реактивные данные
const documents = ref([])
const loading = ref(false)
const totalDocuments = ref(0)
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = ref(10)
const sortBy = ref('date_of_publication')
const sortOrder = ref('desc')
const errorSnackbar = ref(false)
const errorMessage = ref('')

// Параметры из URL
const filterType = computed(() => route.query.type)
const filterLabel = computed(() => route.query.label)
const filterName = computed(() => route.query.name) // Новый параметр
const startDate = computed(() => route.query.startDate)
const endDate = computed(() => route.query.endDate)

// URL для открытия документов
const urlPravoGovRuPath =
  import.meta.env.VITE_PRAVO_GOV_RU_PATH || 'https://publication.pravo.gov.ru/document/'

// Заголовки таблицы
const headers = [
  { title: '№ Документа', key: 'eo_number', width: 150 },
  { title: 'Название', key: 'name', width: 300 },
  { title: 'Тип', key: 'type_name', width: 200 },
  { title: 'Регион', key: 'region_name', width: 200 },
  { title: 'Даты', key: 'dates', width: 150, sortable: false },
  { title: 'Страниц', key: 'pages_count', width: 100 },
  { title: 'Действия', key: 'actions', width: 120, sortable: false }
]

// Опции сортировки
const sortOptions = [
  { text: 'Дата публикации', value: 'date_of_publication' },
  { text: 'Дата подписания', value: 'date_of_signing' },
  { text: 'Дата документа', value: 'document_date' },
  { text: 'Название', value: 'name' },
  { text: 'Заголовок', value: 'title' }
]

// Хлебные крошки
const breadcrumbs = computed(() => [
  { title: 'Главная', to: '/' },
  { title: 'Графики', to: '/charts' },
  { title: 'Детальная таблица', disabled: true }
])

// Лейблы для типов фильтров (расширенные)
const filterTypeLabels = {
  year: 'По году',
  type: 'По типу документа',
  district: 'По федеральному округу',
  region: 'По региону',
  nomenclature: 'По номенклатуре',
  authority: 'По органу власти',
  'district-type': 'Тип документа в ФО',
  'region-type': 'Тип документа в регионе',
  'districts-type-all': 'Тип документа во всех регионах'
}

const filterTypeLabel = computed(() => {
  return filterTypeLabels[filterType.value] || 'Фильтр'
})

// Диапазон дат
const dateRange = computed(() => {
  if (startDate.value && endDate.value) {
    return `${startDate.value} - ${endDate.value}`
  }
  return null
})

// Функции
const openDocument = (eoNumber: string) => {
  if (eoNumber) {
    window.open(urlPravoGovRuPath + eoNumber, '_blank')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

const loadDocuments = async () => {
  loading.value = true

  try {
    const params = {
      type: filterType.value,
      label: filterLabel.value,
      page: currentPage.value,
      page_size: itemsPerPage.value,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    }

    // Добавляем параметр name, если он присутствует
    if (filterName.value) {
      params.name = filterName.value
    }

    if (startDate.value) params.startDate = startDate.value
    if (endDate.value) params.endDate = endDate.value

    const response = await api.table.getDocuments(params)

    const data = response.data
    documents.value = data.documents
    totalDocuments.value = data.total_count
    totalPages.value = data.total_pages
  } catch (error) {
    console.error('Ошибка загрузки документов:', error)
    errorMessage.value = 'Ошибка при загрузке данных. Попробуйте позже.'
    errorSnackbar.value = true
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.go(-1)
}

// Следим за изменениями параметров URL
watch([filterType, filterLabel, filterName, startDate, endDate], () => {
  currentPage.value = 1
  loadDocuments()
})

// Загружаем данные при монтировании
onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.text-truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
