import client from './client'

class Parser {
    endpoint: string
    constructor(endpoint = '/api/parser') {
        this.endpoint = endpoint
    }

    start = async () => {
        return (await client.post(`${this.endpoint}/start`)).data
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

export default Parser
