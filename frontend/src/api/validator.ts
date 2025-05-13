import client from './client'

class Validator {
    endpoint: string
    constructor(endpoint = '/api/validator') {
        this.endpoint = endpoint
    }

    start = async (params: Record<string, any>) => {
        const response = await client.post(`${this.endpoint}/start`, params)

        return {
            status: response.status,
            data: response.data,
        }
    }
    stop = async () => {
        return (await client.post(`${this.endpoint}/stop`)).data
    }
    status = async () => {
        return (await client.get(`${this.endpoint}/status`)).data
    }
    history = async (params: Record<string, number>) => {
        return (await client.get(`${this.endpoint}/history`, { params })).data
    }

    lastRun = async () => {
        return (await client.get(`${this.endpoint}/last-run`)).data
    }
}

export default Validator
