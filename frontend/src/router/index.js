import { createRouter, createWebHistory } from 'vue-router'

import { Dashboard } from '@/components/page'
import { Home } from '@/components/page'
import { Login } from '@/components/page'
import { SignUp } from '@/components/page'

const routes = [
	{ path: '/', name: 'home', component: Home },
	{ path: '/dashboard', name: 'dashboard', component: Dashboard },
	{ path: '/login', name: 'login', component: Login },
	{ path: '/sign-up', name: 'sign-up', component: SignUp },
]

const router = createRouter({
	// 4. Provide the history implementation to use. We are using the hash history for simplicity here.
	history: createWebHistory(),
	routes, // short for `routes: routes`
})

export default router
