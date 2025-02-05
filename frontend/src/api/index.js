import AuthClient from './authClient'
import StatisticsClient from './statisticsClient'
import SubjectsClient from './subjectsClient'

const apiClient = {
	auth: new AuthClient('/auth'),
	statistics: new StatisticsClient('/statistics'),
	subjects: new SubjectsClient('/subjects'),
	
}

export default apiClient
