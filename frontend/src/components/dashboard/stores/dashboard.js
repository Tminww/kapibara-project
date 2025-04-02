import { defineStore } from 'pinia'
import api from '@/api'
import { ref, computed } from 'vue'

export const useDashboardStore = defineStore('dashboard', () => {
    const subjects = ref([])
    const statistics = ref({})

    const emptyResponse = {
        name: '',
        count: 0,
        stat: [], // Пустой массив по умолчанию
        startDate: null,
        endDate: null
    }
    const publicationByYears = ref({ ...emptyResponse })
    const publicationByTypes = ref({ ...emptyResponse })
    const publicationByNomenclature = ref({ ...emptyResponse })
    const publicationByNomenclatureDetail = ref({ ...emptyResponse })

    const publicationByRegionsMin = ref({ ...emptyResponse })
    const publicationByRegionsMax = ref({ ...emptyResponse })

    const publicationByDistricts = ref({ ...emptyResponse })

    const publicationInDistricts = ref({
        name: '',
        count: 0,
        stat: [], // Пустой массив по умолчанию
        districts: [],
        startDate: null,
        endDate: null
    })

    const getSubjects = computed(() => {
        return subjects.value
    })
    const dropRegionsToRequest = () => {
        subjects.value = []
    }

    const loadSubjectsAPI = async (districtName) => {
        const response = await api.subjects.read()
        console.log()
        subjects.value = response.filter((d) => d.name === districtName)[0].regions
    }
    // Геттер для получения регионов в определенном округе
    const getRegionsInDistrict = computed((districtId) => {
        return statistics.value.districts[districtId]
    })

    const getPublicationByDistricts = computed(() => {
        return publicationByDistricts.value.stat
    })

    const getPublicationByDistrictsSeries = computed(() => {
        return publicationByDistricts.value?.stat?.map((row) => row.count)
    })

    const getPublicationByDistrictsLabels = computed(() => {
        return publicationByDistricts.value?.stat?.map((row) => row.name)
    })

    const getPublicationByYears = computed(() => {
        return publicationByYears.value.stat
    })

    const getPublicationByYearsSeries = computed(() => {
        return publicationByYears.value?.stat?.map((row) => row.count)
    })

    const getPublicationByYearsLabels = computed(() => {
        return publicationByYears.value?.stat?.map((row) => row.name)
    })
    const getPublicationByTypes = computed(() => {
        return publicationByTypes.value.stat
    })

    const getPublicationByTypesSeries = computed(() => {
        return publicationByTypes.value?.stat?.map((row) => row.count)
    })

    const getPublicationByTypesLabels = computed(() => {
        return publicationByTypes.value?.stat?.map((row) => row.name)
    })
    const getPublicationByNomenclature = computed(() => {
        return publicationByNomenclature.value.stat
    })

    const getPublicationByNomenclatureSeries = computed(() => {
        return publicationByNomenclature.value?.stat?.map((row) => row.count)
    })

    const getPublicationByNomenclatureLabels = computed(() => {
        return publicationByNomenclature.value?.stat?.map((row) => row.name)
    })

    const getPublicationByNomenclatureDetail = computed(() => {
        return publicationByNomenclatureDetail.value.stat
    })

    const getPublicationByNomenclatureDetailSeries = computed(() => {
        return publicationByNomenclatureDetail.value?.stat
            ?.filter((row) => row.count !== 0) // Пропускаем строки с count == 0
            ?.map((row) => row.count) // Извлекаем только count
    })

    const getPublicationByNomenclatureDetailLabels = computed(() => {
        return publicationByNomenclatureDetail.value?.stat
            ?.filter((row) => row.count !== 0) // Пропускаем строки с count == 0
            ?.map((row) => row.name) // Извлекаем только count
    })

    const getPublicationByNomenclatureDetailTotal = computed(() => {
        return publicationByNomenclatureDetail.value?.count
    })

    const getPublicationByRegionsMin = computed(() => {
        return publicationByRegionsMin.value.stat
    })

    const getPublicationByRegionsMinSeries = computed(() => {
        return publicationByRegionsMin.value?.stat?.map((row) => row.count)
    })

    const getPublicationByRegionsMinLabels = computed(() => {
        return publicationByRegionsMin.value?.stat?.map((row) => row.name)
    })
    const getPublicationByRegionsMax = computed(() => {
        return publicationByRegionsMax.value.stat
    })

    const getPublicationByRegionsMaxSeries = computed(() => {
        return publicationByRegionsMax.value?.stat?.map((row) => row.count)
    })

    const getPublicationByRegionsMaxLabels = computed(() => {
        return publicationByRegionsMax.value?.stat?.map((row) => row.name)
    })

    const getPublicationInRegions = computed(() => {
        return publicationInDistricts.value?.districts?.filter(
            (district) => district.name === districtName
        )?.regions
    })

    const dropPublicationByYears = () => {
        publicationByYears.value = { ...emptyResponse }
    }

    const dropPublicationByDistricts = () => {
        publicationByDistricts.value = { ...emptyResponse }
    }
    const dropPublicationByTypes = () => {
        publicationByTypes.value = { ...emptyResponse }
    }
    const dropPublicationByNomenclature = () => {
        publicationByNomenclature.value = { ...emptyResponse }
    }
    const dropPublicationByNomenclatureDetail = () => {
        publicationByNomenclatureDetail.value = { ...emptyResponse }
    }
    const dropPublicationByRegionsMin = () => {
        publicationByRegionsMin.value = { ...emptyResponse }
    }
    const dropPublicationByRegionsMax = () => {
        publicationByRegionsMax.value = { ...emptyResponse }
    }

    const dropPublicationInDistrict = () => {
        publicationInDistricts.value = {
            name: '',
            count: 0,
            stat: [], // Пустой массив по умолчанию
            districts: [],
            startDate: null,
            endDate: null
        }
    }

    // Обновление статистики через API
    const loadPublicationByDistricts = async (parameters) => {
        try {
            let response = await api.dashboard.readDistricts(parameters)

            publicationByDistricts.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByDistricts()
        }
    }
    // Обновление статистики через API
    const loadPublicationByYears = async (parameters) => {
        try {
            let response = await api.dashboard.readYears(parameters)

            publicationByYears.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByYears()
        }
    }
    const loadPublicationByTypes = async (parameters) => {
        try {
            let response = await api.dashboard.readTypes(parameters)

            publicationByTypes.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByTypes()
        }
    }
    const loadPublicationByNomenclature = async (parameters) => {
        try {
            let response = await api.dashboard.readNomenclature(parameters)

            publicationByNomenclature.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByNomenclature()
        }
    }
    const loadPublicationByNomenclatureDetail = async (parameters) => {
        try {
            let response = await api.dashboard.readNomenclatureDetail(parameters)

            publicationByNomenclatureDetail.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByNomenclatureDetail()
        }
    }
    const loadPublicationByRegionsMin = async (parameters) => {
        try {
            parameters.sort = 'min'
            parameters.limit = 10

            let response = await api.dashboard.readRegions(parameters)

            publicationByRegionsMin.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByRegionsMin()
        }
    }
    const loadPublicationByRegionsMax = async (parameters) => {
        try {
            parameters.sort = 'max'
            parameters.limit = 10

            let response = await api.dashboard.readRegions(parameters)

            publicationByRegionsMax.value = response.data
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationByRegionsMax()
        }
    }

    const loadPublicationInDistricts = async (districtName, parameters) => {
        try {
            parameters.districtName = districtName
            let response = await api.statistics.readDistricts(parameters)
            console.log(districtName, response.districts)
            publicationInDistricts.value = response.data.districts.filter(
                (d) => d.name === districtName
            )[0].regions
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error)
            dropPublicationInDistrict()
        }
    }

    const loadSubjectStatisticsAPI = async (parameters) => {
        statistics.value = await api.statistics.read(parameters)
    }

    return {
        getPublicationByYears,
        getPublicationByTypes,
        getPublicationByNomenclature,
        getPublicationByNomenclatureDetail,
        getPublicationByRegionsMin,
        getPublicationByRegionsMax,
        getPublicationByDistricts,

        dropPublicationByYears,
        dropPublicationByTypes,
        dropPublicationByNomenclature,
        dropPublicationByNomenclatureDetail,
        dropPublicationByRegionsMin,
        dropPublicationByRegionsMax,
        dropPublicationByDistricts,

        loadPublicationByYears,
        loadPublicationByTypes,
        loadPublicationByNomenclature,
        loadPublicationByNomenclatureDetail,
        loadPublicationByRegionsMin,
        loadPublicationByRegionsMax,
        loadPublicationByDistricts,

        getPublicationByNomenclatureSeries,
        getPublicationByNomenclatureDetailSeries,
        getPublicationByYearsSeries,
        getPublicationByDistrictsSeries,
        getPublicationByRegionsMinSeries,
        getPublicationByRegionsMaxSeries,
        getPublicationByTypesSeries,

        getPublicationByNomenclatureLabels,
        getPublicationByNomenclatureDetailLabels,
        getPublicationByYearsLabels,
        getPublicationByDistrictsLabels,
        getPublicationByRegionsMinLabels,
        getPublicationByRegionsMaxLabels,
        getPublicationByTypesLabels,

        getPublicationByNomenclatureDetailTotal,

        getPublicationInRegions,
        dropPublicationInDistrict,
        loadPublicationInDistricts,
        getRegionsInDistrict,
        getSubjects,
        dropRegionsToRequest,
        loadSubjectsAPI,
        loadSubjectStatisticsAPI
    }
})
