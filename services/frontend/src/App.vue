<template>
    <v-app>

        <v-row>
            <v-col>
                <v-container>
                    <v-app-bar color="primary" prominent>
                        <template v-slot:prepend>
                            <v-app-bar-nav-icon @click.stop="leftMenu = !leftMenu"></v-app-bar-nav-icon>
                        </template>
                        <v-toolbar-title>Отображение статистики</v-toolbar-title>
                    </v-app-bar>

                    <v-navigation-drawer v-model="leftMenu" location="left" temporary :width="400">

                        <v-container>
                            <div v-if="errorSubjects">
                                {{ errorSubjects }}
                            </div>
                            <template v-else>
                                <div v-if="loadingSubjests" class="d-flex align-center justify-center">
                                    <v-progress-circular indeterminate />
                                </div>

                                <template v-else>
                                    <request-form @loading-successful="leftMenu = false, resultIsEmpty = false"
                                        @loading-error="leftMenu = false, resultIsEmpty = true"
                                        :districts="getRegionsToRequest" />
                                </template>
                            </template>
                        </v-container>
                    </v-navigation-drawer>
                </v-container>
            </v-col>
        </v-row>

        <v-row>


            <v-col>
                <template v-if="resultIsEmpty">
                    <v-row>
                        Нет результатов
                    </v-row>
                </template>

                <template v-else>
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
                </template>

            </v-col>
        </v-row>
        <v-footer class="text-center d-flex flex-column" color="primary">


            <div>
                {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
            </div>

        </v-footer>
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
            leftMenu: false,
            resultIsEmpty: false,
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
        // draver() {
        //     if (this.leftMenu) {

        //     }
        //     return this.leftMenu && !this.loadingStatistics
        // }
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
    watch: {
        group() {
            this.leftMenu = false
        },
    },
    async mounted() {
        await this.loadSubjects()
        await this.loadStatistics()
    },
}
</script>

<style scoped></style>
