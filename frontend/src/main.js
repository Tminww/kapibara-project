import App from '@/app/App.vue'

import { createApp } from 'vue'

import './assets/style.css'

import { createPinia } from 'pinia'

import VueApexCharts from 'vue3-apexcharts'

import vuetify from '@/plugins/vuetify'

import i18n from '@/plugins/i18n'

import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(i18n)
app.use(VueApexCharts)
app.mount('#app')
