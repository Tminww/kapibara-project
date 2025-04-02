import client from './client';

class Statistics {
  constructor(endpoint = '/api/statistics') {
    this.endpoint = endpoint;
  }

  // Получение общей статистики
  read = async function (params = {}) {
    return (await client.get(this.endpoint, { params })).data;
  };

  // Получение статистики по округам
  readDistricts = async function (params = {}) {
    return (await client.get(`${this.endpoint}/districts`, { params })).data;
  };

  // Получение статистики по конкретному округу
  readDistrictById = async function (distId, params = {}) {
    return (await client.get(`${this.endpoint}/districts/${String(distId)}`, { params })).data;
  };
}

export default Statistics;