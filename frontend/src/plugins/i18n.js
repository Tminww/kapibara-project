import { createI18n } from 'vue-i18n'
import { default as ru } from '../locales/ru.json'

const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'ru',
    fallbackLocale: 'ru',
    messages: {
        ru
    }
})

export default i18n
