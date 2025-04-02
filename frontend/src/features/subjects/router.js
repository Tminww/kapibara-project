const meta = {
    requiresAuth: false,
    forAdmin: false,
    forUser: false,
    forAll: true
}

export const routes = [
    {
        path: '/subjects',
        name: 'subjects',
        component: () => import('./pages/DistrictPage.vue'),
        meta: {
            ...meta,
            breadCrumb: [
                {
                    text: 'Главная',
                    to: { name: 'home' }
                },
                {
                    text: 'Субъекты ОГВ'
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
                    text: 'Субъекты ОГВ',
                    to: { name: 'subjects' }
                },
                {
                    text: 'Федеральные округа'
                }
            ]
        }
    }
]
