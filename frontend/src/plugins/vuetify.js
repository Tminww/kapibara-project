import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/lib/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import { ru, en } from 'vuetify/locale'

const vuetify = createVuetify({
	locale: {
		locale: 'ru',
		fallback: 'en',
		messages: { ru, en },
	},
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

export default vuetify
