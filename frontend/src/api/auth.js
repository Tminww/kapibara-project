import apiClient from './base.js.deprecated'

export async function login(data) {
	return (await apiClient.post('/auth/login', data)).data
}
