import { Forbidden403, NotFound404 } from '@/pages/errors'

const meta = {
	requiresAuth: false,
	forAdmin: false,
	forUser: false,
	forAll: true,
}

const errorRoutes = [
	{
		path: '/forbidden',
		name: 'forbidden',
		component: Forbidden403,
		meta,
	},
	{
		path: '/:pathMatch(.*)*',
		name: 'not-found',
		component: NotFound404,
		meta,
	},
]

export default errorRoutes
