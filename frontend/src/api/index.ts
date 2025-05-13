import Statistics from './statistics'
import Subjects from './subjects'
import Dashboard from './dashboard'
import Parser from './parser'
import Validator from './validator'
import Auth from './auth'

const api = {
    statistics: new Statistics('/statistics'),
    subjects: new Subjects('/subjects'),
    dashboard: new Dashboard('/dashboard'),
    parser: new Parser('/parser'),
    validator: new Validator('/validator'),
    auth: new Auth('/auth')
}

export default api
