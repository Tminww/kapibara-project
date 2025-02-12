import { DashboardPage } from '@/pages'
import { DistrictPage } from '@/pages'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

const dashboardRoutes = [
	{
		path: '/dashboard',
		name: 'dashboard',
		component: DashboardPage,
		meta,
	},
	{
		path: '/dashboard/:label',
		name: 'district',
		component: DistrictPage,
		meta,
	},
]

export default dashboardRoutes
