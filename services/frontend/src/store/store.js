import { createStore } from 'vuex'
import {
	getAllStatistics,
	getAllSubjects,
	updateSatistics,
} from '../api/statistics.js'

const store = createStore({
	state() {
		return {
			statistics: {},
			regionsToRequest: [],
			regionsFromDistrict: [],
		}
	},
	getters: {
		getRegionsInDistrict(state, districtId) {
			return state.statistics.districts[districtId]
		},

		getAllStatistics(state) {
			return {
				name: state.statistics.name,
				count: state.statistics.count,
				stat: state.statistics.stat,
			}
		},

		getDistricts(state) {
			return state.statistics.districts
		},

		getStatistics(state) {
			return state.statistics
		},
		getRegionsToRequest(state) {
			return state.regionsToRequest
		},
	},
	mutations: {
		setStatistics(state, newValue) {
			// if (Array.isArray(newValue)) {
			//     state.statistics = newValue
			// }
			state.statistics = newValue
		},

		setRegionsToRequest(state, newValue) {
			// if (Array.isArray(newValue)) {
			//     state.statistics = newValue
			// }
			state.regionsToRequest = newValue
		},
	},
	actions: {
		setStatistics(context, newValue) {
			context.commit('setStatistics', newValue)
		},
		setRegionsToRequest(context, newValue) {
			context.commit('setRegionsToRequest', newValue)
		},

		dropStatistics(context) {
			context.commit('setStatistics', [])
		},
		dropRegionsToRequest(context) {
			context.commit('setRegionsToRequest', [])
		},
		async loadStatisticsAPI(context) {
			const statistics = await getAllStatistics()
			context.commit('setStatistics', statistics)
		},
		async updateStatisticsAPI(context, parameters) {
			const statistics = await updateSatistics(parameters)
			context.commit('setStatistics', statistics)
		},
		async loadSubjectsAPI(context) {
			const regionsToRequest = await getAllSubjects()
			context.commit('setRegionsToRequest', regionsToRequest)
		},
	},
})

export default store
