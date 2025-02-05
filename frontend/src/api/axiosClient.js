import axios from 'axios'

const axiosClient = axios.create({
	baseURL:
		import.meta.env.VITE_MODE === 'DEV'
			? import.meta.env.VITE_DEV_PATH
			: import.meta.env.VITE_PROD_PATH,
	'Content-Type': 'application/json',
})

if (localStorage.getItem('token') !== null) {
	axiosClient.defaults.withCredentials = true
	axiosClient.defaults.headers.common['Authorization'] =
		`Bearer ${localStorage.getItem('token')}`
}

export default axiosClient
