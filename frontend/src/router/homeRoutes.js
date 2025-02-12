import { HomePage } from '@/pages'
import { DashboardPage } from '@/pages'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

const homeRoutes = [
	{
		path: '/',
		name: 'home',
		component: DashboardPage,
		meta,
	},
]

export default homeRoutes
