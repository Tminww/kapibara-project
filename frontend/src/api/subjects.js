import client from './client';

class Subjects {
  constructor(endpoint = '/api/subjects') {
    this.endpoint = endpoint;
  }

  // Получение списка субъектов
  read = async function () {
    return (await client.get(this.endpoint)).data;
  };

  // Получение регионов с фильтрацией по districtName или districtId
  readRegions = async function (params = {}) {
    return (await client.get(`${this.endpoint}/regions`, { params })).data;
  };

  // Получение округов
  readDistricts = async function (params = {}) {
    return (await client.get(`${this.endpoint}/districts`, { params })).data;
  };
}

export default Subjects;