import axios from 'axios'
import statistics from '../mock/statistics.json'
import subjects from '../mock/subjects.json'

// axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'https://kapi.tminww.site/api/'
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

export async function getAllStatistics() {
	return (await axios.get('/statistics?regions=12')).data
}

export async function updateSatistics(parameters) {
	const params = new URLSearchParams(parameters)
	console.log(params)
	console.log('URL', `http://localhost:8080/statistics?${params}`)
	return (await axios.get(`/statistics?${params}`)).data
	// return (await axios.get(`/statistics`, parameters)).data
}

export async function getAllSubjects() {
	return (await axios.get('/subjects')).data
}
