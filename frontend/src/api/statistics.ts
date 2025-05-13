import client from './client'

class Statistics {
    endpoint: string
    constructor(endpoint = '/api/statistics') {
        this.endpoint = endpoint
    }

    // Получение общей статистики
    read = async (params: Record<string, string>) => {
        return (await client.get(this.endpoint, { params })).data
    }

    // Получение статистики по округам
    readDistricts = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/districts`, { params })).data
    }

    // Получение статистики по конкретному округу
    readDistrictById = async (distId: number, params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/districts/${String(distId)}`, { params })).data
    }
}

export default Statistics
