import axiosClient from './axiosClient'

class StatisticsClient {
	constructor(endpoint) {
		this.endpoint = endpoint
	}
	read = async function (params = {}) {
		return (await axiosClient.get(this.endpoint, { params })).data
	}
	readOneDistrict = async function (id, params = {}) {
		return (await axiosClient.get(this.endpoint + '/' + String(id), params))
			.data
	}
	readOneRegion = async function (id, params = {}) {
		return (
			await axiosClient.get(
				this.endpoint + '?regions=' + String(id),
				params,
			)
		).data
	}
}

export default StatisticsClient
