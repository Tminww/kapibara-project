import client from './client'

class Subjects {
    endpoint: string
    constructor(endpoint = '/api/subjects') {
        this.endpoint = endpoint
    }

    // Получение списка субъектов
    read = async () => {
        return (await client.get(this.endpoint)).data
    }

    // Получение регионов с фильтрацией по districtName или districtId
    readRegions = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/regions`, { params })).data
    }

    // Получение округов
    readDistricts = async () => {
        return (await client.get(`${this.endpoint}/districts`)).data
    }
}

export default Subjects
