<template>
    <v-app>
        <v-row>
            <v-col>
                <v-container>
                    <v-app-bar scroll-behavior="collapse" color="primary" prominent>
                        <template v-slot:prepend>
                            <v-app-bar-nav-icon @click="navBarClicked = !navBarClicked"></v-app-bar-nav-icon>
                        </template>
                        <v-toolbar-title>Отображение статистики</v-toolbar-title>

                        <v-btn variant="text" icon="mdi-dots-vertical"></v-btn>
                    </v-app-bar>
                </v-container>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="3" v-if="navBarClicked">
                <v-container>
                    <template v-if="errorSubjects">
                        {{ errorSubjects }}
                    </template>
                    <template v-else>
                        <div v-if="loadingSubjests" class="d-flex align-center justify-center">
                            <v-progress-circular indeterminate />
                        </div>

                        <template v-else>
                            <request-form :districts="getRegionsToRequest" />
                        </template>
                    </template>
                </v-container>
            </v-col>
            <v-divider class="mx-3" vertical dark></v-divider>

            <v-col>
                <v-container>
                    <v-row>
                        <v-col v-if="errorStatistics">
                            {{ errorStatistics }}
                        </v-col>
                        <template v-else>
                            <v-col v-if="loadingStatistics" class="d-flex align-center justify-center">
                                <v-progress-circular indeterminate />
                            </v-col>
                            <template v-else>
                                <v-col>
                                    <stat-all-card :all="this.getAllStatistics" />
                                </v-col>

                                <v-col v-for="district in this.getDistricts">
                                    <stat-district-card :district="district" />
                                </v-col>
                            </template>
                        </template>
                    </v-row>
                </v-container>
            </v-col>
        </v-row>
    </v-app>
</template>

<script lang="js">
import { mapGetters, mapActions } from 'vuex'
import { StatDistrictCard, StatAllCard, RequestForm } from './components/widget'
export default {
    name: 'app',
    components: { StatDistrictCard, RequestForm, StatAllCard },

    data() {
        return {
            loadingStatistics: false,
            loadingSubjests: false,
            errorStatistics: null,
            errorSubjects: null,
            navBarClicked: false,
        }
    },
    computed: {
        ...mapGetters([
            'getStatistics',
            'getRegionsToRequest',
            'getRegionsInDistrict',
            'getDistricts',
            'getAllStatistics',
        ]),
    },

    methods: {
        ...mapActions([
            'dropStatistics',
            'dropRegionsToRequest',
            'loadSubjectsAPI',
            'loadStatisticsAPI',
        ]),
        async loadStatistics() {
            try {
                this.loadingStatistics = true
                this.error = null
                await this.loadStatisticsAPI()
            } catch (e) {
                this.error = e.message
                this.dropStatistics()
            } finally {
                this.loadingStatistics = false
            }
        },

        async loadSubjects() {
            try {
                this.loadingSubjests = true
                this.error = null
                await this.loadSubjectsAPI()
            } catch (e) {
                this.error = e.message
                this.dropRegionsToRequest()
            } finally {
                this.loadingSubjests = false
            }
        },
    },

    async mounted() {
        await this.loadSubjects()
        await this.loadStatistics()
    },
}
</script>

<style scoped>
.main-container {
    margin-top: 100px;
}
</style>
