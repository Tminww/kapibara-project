import axiosClient from './axiosClient'

class SubjectsClient {
	constructor(endpoint) {
		this.endpoint = endpoint
	}
	read = async function (params = {}) {
		console.log('CRUD GET: ' + this.endpoint + { params })
		return (await axiosClient.get(this.endpoint, params)).data
	}
	readOne = async function (id, params = {}) {
		console.log('CRUD GET ONE: ' + this.endpoint + { params })
		return (
			await axiosClient.get(this.endpoint + '/' + String(id), params)
		).data
	}
	
}

export default SubjectsClient
