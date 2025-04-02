import Statistics from './statistics'
import Subjects from './subjects'
import Dashboard from './dashboard'


const api = {
	statistics: new Statistics('/statistics'),
	subjects: new Subjects('/subjects'),
	dashboard: new Dashboard('/dashboard'),
}

export default api
