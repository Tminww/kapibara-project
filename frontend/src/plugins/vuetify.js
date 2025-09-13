import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import { ru, en } from 'vuetify/locale'

const vuetify = createVuetify({
  locale: {
    locale: 'ru',
    fallback: 'en',
    messages: { ru, en }
  },

  theme: {
    defaultTheme: 'custom',
    themes: {
      custom: {
        dark: false,
        colors: {
          primary: '#1d4c86',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          // info: '#2196F3',
          info: '#1d4c86',
          success: '#4CAF50',
          warning: '#FFC107'
        }
      }
    }
  },

  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  },
  components,
  directives
})

export default vuetify
