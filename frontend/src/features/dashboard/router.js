import { DashboardPage } from './pages/'
import { DistrictPage } from './pages/'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

export const routes = [
	{
		path: '/',
		name: 'dashboard',
		component: DashboardPage,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Информационная панель',
				},
			],
		},
	},
	{
		path: '/dashboard/:label',
		name: 'district',
		component: DistrictPage,
		meta: {
			...meta,
			breadCrumb: [
				{
					text: 'Главная',
					to: { name: 'home' },
				},
				{
					text: 'Информационная панель',
					to: { name: 'dashboard' },
				},
				{
					text: '',
				},
			],
		},
		beforeEnter: (to, from, next) => {
			// Устанавливаем значение label в meta.breadCrumb
			to.meta.breadCrumb[2].text = to.params.label
			next()
		},
	},
]
