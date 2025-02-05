import { createApp } from 'vue'
import './assets/style.css'
import App from './App.vue'
import { createPinia } from 'pinia'

import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/lib/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import VueApexCharts from 'vue3-apexcharts'

const vuetify = createVuetify({
	theme: {
		defaultTheme: 'light',
	},
	icons: {
		defaultSet: 'mdi',
		aliases,
		sets: {
			mdi,
		},
	},
	components,
	directives,
})

const app = createApp(App)
app.use(createPinia())
app.use(vuetify)
app.use(VueApexCharts)
app.mount('#app')
