import client from './client'

class Dashboard {
    constructor(endpoint = '/api/dashboard') {
        this.endpoint = endpoint
    }

    // Получение статистики по номенклатуре
    readNomenclature = async function (params = {}) {
        return (await client.get(`${this.endpoint}/nomenclature`, { params })).data
    }

    // Получение статистики по номенклатуре
    readNomenclatureDetail = async function (params = {}) {
        params.detail = 'True'
        return (await client.get(`${this.endpoint}/nomenclature`, { params })).data
    }

    // Получение статистики по годам
    readYears = async function (params = {}) {
        return (await client.get(`${this.endpoint}/years`, { params })).data
    }

    // Получение статистики по округам
    readDistricts = async function (params = {}) {
        return (await client.get(`${this.endpoint}/districts`, { params })).data
    }

    // Получение статистики по регионам
    readRegions = async function (params = {}) {
        return (await client.get(`${this.endpoint}/regions`, { params })).data
    }

    // Получение статистики по типам
    readTypes = async function (params = {}) {
        return (await client.get(`${this.endpoint}/types`, { params })).data
    }
}

export default Dashboard
