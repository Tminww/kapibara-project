import { LoginPage } from '@/pages'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

const loginRoutes = [
	{
		path: '/login',
		name: 'login',
		component: LoginPage,
		meta,
	},
]

export default loginRoutes
