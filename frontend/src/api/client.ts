import axios from 'axios'

const client = axios.create({
    baseURL:
        import.meta.env.VITE_MODE === 'DEV'
            ? import.meta.env.VITE_DEV_PATH
            : import.meta.env.VITE_PROD_PATH,
    headers: {
        'Content-Type': 'application/json'
    }
})

if (localStorage.getItem('token') !== null) {
    client.defaults.withCredentials = true
    client.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
}

export default client
