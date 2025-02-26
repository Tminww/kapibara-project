import { DashboardPage } from './pages/'

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
]
