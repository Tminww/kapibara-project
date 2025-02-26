import AuthClient from './authClient'
import StatisticsClient from './statisticsClient'
import SubjectsClient from './subjectsClient'

const apiClient = {
	auth: new AuthClient('/auth'),
	statistics: new StatisticsClient('/statistics'),
	subjects: new SubjectsClient('/subjects'),
	publicationByNomenclature: new StatisticsClient(
		'statistics/publication-by-nomenclature',
	),
	publicationByNomenclatureDetail: new StatisticsClient(
		'statistics/publication-by-nomenclature-detail',
	),
	publicationByYears: new StatisticsClient('statistics/publication-by-years'),
	publicationByDistricts: new StatisticsClient(
		'statistics/publication-by-districts',
	),
	publicationByRegions: new StatisticsClient(
		'statistics/publication-by-regions',
	),
}

export default apiClient
