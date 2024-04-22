import http from './http'

const users = {
	async getUserData(params) {
		return await http.get('/api/users/user', params)
	},
}
