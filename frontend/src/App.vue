<template>
	<v-app>
		<v-row>
			<v-col>
				<v-container>
					<v-app-bar color="primary" prominent>
						<template v-slot:prepend>
							<v-app-bar-nav-icon
								@click.stop="leftMenu = !leftMenu"
							></v-app-bar-nav-icon>
						</template>
						<v-toolbar-title>Капибара</v-toolbar-title>
					</v-app-bar>

					<v-navigation-drawer
						v-model="leftMenu"
						location="left"
						temporary
						:width="500"
					>
						<v-container>
							<div v-if="errorSubjects">
								<v-alert
									class="d-flex align-center justify-center"
									type="error"
									title="Произошла ошибка"
									:text="errorSubjects"
									variant="tonal"
								></v-alert>
							</div>
							<template v-else>
								<div
									v-if="loadingSubjests"
									class="d-flex align-center justify-center"
								>
									<v-progress-circular indeterminate />
								</div>

								<template v-else>
									<request-form
										@loading-successful="
											((leftMenu = false),
											(resultIsEmpty = false))
										"
										@loading-error="
											((leftMenu = false),
											(resultIsEmpty = true))
										"
										:districts="
											subjectStore.getRegionsToRequest
										"
									/>
								</template>
							</template>
						</v-container>
					</v-navigation-drawer>
				</v-container>
			</v-col>
		</v-row>

		<v-row>
			<v-col v-if="emptyRequest">
				<v-alert
					class="d-flex align-center justify-center"
					type="warning"
					title="Предупреждение"
					text="Нет результатов"
					variant="tonal"
				></v-alert>
			</v-col>
			<template v-else>
				<v-col>
					<v-container>
						<v-row>
							<v-col v-if="errorStatistics">
								<v-alert
									class="d-flex align-center justify-center"
									type="error"
									title="Произошла ошибка"
									:text="errorStatistics"
									variant="tonal"
								></v-alert>
							</v-col>
							<template v-else>
								<v-col
									v-if="loadingStatistics"
									class="d-flex align-center justify-center"
								>
									<v-progress-circular indeterminate />
								</v-col>
								<template v-else>
									<v-col>
										<stat-all-card
											:all="statisticStore.getStatistics"
										/>
									</v-col>

									<v-col
										v-for="district in statisticStore.getDistricts"
									>
										<stat-district-card
											:district="district"
										/>
									</v-col>
								</template>
							</template>
						</v-row>
					</v-container>
				</v-col>
			</template>
		</v-row>
		<!-- <v-footer class="text-center d-flex flex-column" color="primary" height="200">


            <div>
                {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
            </div>

        </v-footer> -->
	</v-app>
</template>

<script setup>
	import { ref, computed, onMounted, watchEffect } from 'vue'
	import {
		StatDistrictCard,
		StatAllCard,
		RequestForm,
	} from './components/widget'
	import { useStatisticStore, useSubjectStore } from './stores/'
	import { getLastQuarter } from './utils/utils.js'

	const statisticStore = useStatisticStore()
	const subjectStore = useSubjectStore()

	const loadingStatistics = ref(false)
	const loadingSubjests = ref(false)
	const errorStatistics = ref(null)
	const errorSubjects = ref(null)
	const leftMenu = ref(false)
	const resultIsEmpty = ref(false)

	const emptyRequest = computed(() => {
		console.log('NO RESULT', resultIsEmpty.value)
		return resultIsEmpty.value
	})

	const loadStatistics = async () => {
		try {
			loadingStatistics.value = true
			errorStatistics.value = null
			console.log('FUNC', getLastQuarter())
			const parameters = getLastQuarter()

			await statisticStore.updateStatisticsAPI(parameters)
		} catch (e) {
			errorStatistics.value = e.message
			statisticStore.dropStatistics()
		} finally {
			loadingStatistics.value = false
		}
	}

	const loadSubjects = async () => {
		try {
			loadingSubjests.value = true
			errorSubjects.value = null
			await subjectStore.loadSubjectsAPI()
		} catch (e) {
			errorSubjects.value = e.message
			subjectStore.dropRegionsToRequest()
		} finally {
			loadingSubjests.value = false
		}
	}

	watchEffect(() => {
		leftMenu.value = false
	})

	onMounted(async () => {
		await loadSubjects()
		await loadStatistics()
	})
</script>

<style scoped></style>
