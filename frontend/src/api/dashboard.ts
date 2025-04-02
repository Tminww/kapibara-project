import client from './client'

class Dashboard {
    endpoint: string

    constructor(endpoint = '/api/dashboard') {
        this.endpoint = endpoint
    }

    // Получение статистики по номенклатуре
    readNomenclature = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/nomenclature`, { params })).data
    }

    // Получение статистики по номенклатуре
    readNomenclatureDetail = async (params: Record<string, string>) => {
        params.detail = 'True'
        return (await client.get(`${this.endpoint}/nomenclature`, { params })).data
    }

    // Получение статистики по годам
    readYears = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/years`, { params })).data
    }

    // Получение статистики по округам
    readDistricts = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/districts`, { params })).data
    }

    // Получение статистики по регионам
    readRegions = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/regions`, { params })).data
    }

    // Получение статистики по типам
    readTypes = async (params: Record<string, string>) => {
        return (await client.get(`${this.endpoint}/types`, { params })).data
    }
}

export default Dashboard
