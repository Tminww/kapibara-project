import axios from 'axios'
// axios.defaults.withCredentials = true;
// axios.defaults.baseURL = 'http://localhost:8080/'
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

const http = {
	baseUrl: 'http://localhost:8080',
	async get(path, params) {
		console.log(this.baseUrl, path, params)
		return (await axios.get(`${this.baseUrl}/${path}/${params}`)).data
	},
	async post(path, body) {
		return
	},
	setUrl(url) {
		this.baseUrl = url
	},
}

export { http }
export default http
