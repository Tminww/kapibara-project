import axiosClient from './axiosClient'

class AuthClient {
	constructor(endpoint) {
		this.endpoint = endpoint
	}
	login = async function (data) {
		console.log('AUTH LOGIN: ' + this.endpoint + '/login')

		return (await axiosClient.post(`${this.endpoint}/login`, data))
			.data
	}
}

export default AuthClient
