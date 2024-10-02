import http from './http'
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8080/'
const statistics = {
	async getAllSubjects() {
		return await http.get('subjects')
	},
	async getAllStatistics() {
		return await http.get('')
	},
	async updateSatistics(parameters) {
		const params = new URLSearchParams(parameters)
		console.log(params)
		console.log('URL', `http://localhost:8080/statistics?${params}`)
		return (await http.get(`statistics/`, `${params}`)).data
		// return (await axios.get(`/statistics`, parameters)).data
	},
}

export { statistics }
export default statistics

export async function getAllStatistics() {
	return (await axios.get('/statistics?regions=12')).data
}

export async function getAllSubjects() {
	return (await axios.get('/subjects')).data
}

export async function updateSatistics(parameters) {
	const params = new URLSearchParams(parameters)
	console.log(params)
	console.log('URL', `http://localhost:8080/statistics?${params}`)
	return (await axios.get(`/statistics?${params}`)).data
	// return (await axios.get(`/statistics`, parameters)).data
}
