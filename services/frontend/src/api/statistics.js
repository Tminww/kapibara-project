import axios from 'axios'
import statistics from '../mock/statistics.json'
import subjects from '../mock/subjects.json'

// axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8080/'
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

export async function getAllStatistics() {
	if (import.meta.env.VITE_USE_MOCK_DATA) {
		return await new Promise(resolve =>
			setTimeout(() => resolve(statistics), 1000),
		)
	} else {
		return (await axios.get('/statistics')).data
	}
}

export async function getAllSubjects() {
	if (import.meta.env.VITE_USE_MOCK_DATA) {
		return await new Promise(resolve =>
			setTimeout(() => resolve(subjects), 1000),
		)
	} else {
		return (await axios.get('/subjects')).data
	}
}

export async function updateSatistics(parameters) {
	// const config = {
	// 	params: {
	// 		regions: parameters.regions == null ? null : parameters.regions,
	// 		start_date:
	// 			parameters.start_date == null ? null : parameters.start_date,

	// 		end_date: parameters.end_date == null ? null : parameters.end_date,
	// 	},
	// }

	const params = new URLSearchParams(parameters)
	console.log(params)

	// console.log('API Conf', config)
	return (
		await axios
			.get(`/statistics?${params}`)
			.then(function (response) {
				console.log(response)
			})
			.catch(function (error) {
				console.log(error)
			})
	).data
}
