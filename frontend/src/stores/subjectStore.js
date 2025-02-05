import { defineStore } from 'pinia'
import apiClient from '@/api'
import { ref, computed } from 'vue'

export const useSubjectStore = defineStore('subject', () => {
	const regionsToRequest = ref([])

	const getRegionsToRequest = computed(() => {
		return regionsToRequest.value
	})

	const setRegionsToRequest = newValue => {
		regionsToRequest.value = newValue
	}

	const dropRegionsToRequest = () => {
		regionsToRequest.value = []
	}

	const loadSubjectsAPI = async () => {
		const subjects = await apiClient.subjects.read()
		regionsToRequest.value = subjects
	}
	return {
		regionsToRequest,
		getRegionsToRequest,
		setRegionsToRequest,
		dropRegionsToRequest,
		loadSubjectsAPI,
	}
})
