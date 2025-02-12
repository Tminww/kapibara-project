import { HomePage } from '@/pages'

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
		component: HomePage,
		meta,
	},
]

export default homeRoutes
