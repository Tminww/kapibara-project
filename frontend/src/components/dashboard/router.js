import { DashboardPage } from './pages'
import { DistrictPage } from './pages'
import { RegionPage } from './pages'

const meta = {
    requiresAuth: true,
    forAdmin: false,
    forUser: false,
    forAll: true
}

export const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: () => import('./pages/DashboardPage.vue'),
        meta: {
            ...meta,
            breadCrumb: [
                {
                    text: 'Главная',
                    to: { name: 'home' }
                },
                {
                    text: 'Информационная панель'
                }
            ]
        }
    },
    {
        path: '/dashboard/districts/',
        name: 'district',
        component: () => import('./pages/DistrictPage.vue'),
        meta: {
            ...meta,
            breadCrumb: [
                {
                    text: 'Главная',
                    to: { name: 'home' }
                },
                {
                    text: 'Информационная панель',
                    to: { name: 'dashboard' }
                },
                {
                    text: 'Федеральные округа'
                }
            ]
        }
    },
    {
        path: '/dashboard/districts/:id',
        name: 'region',
        component: () => import('./pages/RegionPage.vue'),

        meta: {
            ...meta,
            breadCrumb: [
                {
                    text: 'Главная',
                    to: { name: 'home' }
                },
                {
                    text: 'Информационная панель',
                    to: { name: 'dashboard' }
                },
                {
                    text: ''
                }
            ]
        },
        beforeEnter: (to, from, next) => {
            // Устанавливаем значение label в meta.breadCrumb
            to.meta.breadCrumb[2].text = to.query.label
            next()
        }
    }
]
