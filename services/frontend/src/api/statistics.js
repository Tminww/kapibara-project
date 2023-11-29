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
