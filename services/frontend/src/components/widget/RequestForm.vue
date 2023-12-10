<template>
    <v-form @submit.prevent="onFormSubmit()">

        <div v-for="district in districts" :key="district.id">
            <v-select cache-items density="comfortable" clearable multiple variant="outlined"
                @update:modelValue="e => selectModelUpdate(district.id, e)" :label="district.name" item-title="name"
                item-value="id" :items="getSubjectItemsAndId(district)">
                <template v-slot:selection="{ item, index }">
                    <div v-if="index < 1">
                        <span>{{ item.title }}</span>
                    </div>
                    <span v-if="index === 1" class="text-grey text-caption align-self-center">
                        (+{{ selectedSubjects[district.id].length - 1 }} другие)
                    </span>
                </template>
            </v-select>
        </div>



        <v-divider class="mb-5"></v-divider>

        <v-select density="comfortable" variant="outlined" @update:modelValue="e => comboBoxModelUpdate(e)"
            label="Выбор периода" :items="[
                'За прошлый месяц',
                'За прошлый квартал',
                'За прошлый год',]">
        </v-select>

        <v-row>

            <v-col>
                <v-text-field @update:modelValue="e => startDateModelUpdate(e)" placeholder="yyyy-mm-dd" density="default"
                    variant="solo" type="date" :value="startDate">
                    <!-- {{ startDate }} -->
                </v-text-field>

            </v-col>
            <v-col>
                <v-text-field @update:modelValue="e => endDateModelUpdate(e)" placeholder="yyyy-mm-dd" density="default"
                    variant="solo" type="date" :value="endDate">
                    <!-- {{ endDate }} -->
                </v-text-field>

            </v-col>

        </v-row>
        <v-row>
            <v-col>
                <v-btn type=" submit" :loading="loadingStatistics" text="Применить" />
            </v-col>
        </v-row>



    </v-form>
    <div v-if="errorStatistics">{{ errorStatistics }}</div>
</template>

<script lang="js">
// import RequestSelect from './RequestSelect.vue'
// import DatePicker from './DatePicker.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
    name: 'request-form',
    components: {},
    props: {
        districts: { type: Object, required: true },
    },
    emits: ['loadingSuccessful', 'loadingError'],

    data() {
        return {
            loadingStatistics: false,
            errorStatistics: null,
            startDate: null,
            endDate: null,
            selectedSubjects: {},

        }
    },
    computed: {
        ...mapGetters(["getStatistics"]),

    },

    methods: {
        ...mapActions(['updateStatisticsAPI', 'dropStatistics']),
        getSubjectItemsAndId(district) {
            let regionInfo = []
            for (const region of district.regions) {
                regionInfo.push({ name: region.name, id: region.id })
            }
            return regionInfo
        },

        paramsProcessing(selected, startDate, endDate) {
            const params = {};
            if (startDate !== null) {
                params["start_date"] = startDate;
            }
            if (endDate !== null) {
                params["end_date"] = endDate;
            }

            const subjects = [];
            for (const subjectsInDistrict of Object.values(selected)) {
                for (const subjectId of subjectsInDistrict) {
                    subjects.push(subjectId)
                }
            }
            if (subjects.length > 0) {
                params["regions"] = subjects.toString();
            }
            return params

        },
        dateFormat(date) {

            const year = date.getFullYear();
            const month = date.getMonth() >= 9 ? date.getMonth() + 1 : "0" + (date.getMonth() + 1);
            const day = date.getDate() >= 9 ? date.getDate() : "0" + date.getDate();
            console.log(`${year}-${month}-${day}`)
            return `${year}-${month}-${day}`
        },
        setDefaultValue() {
            this.loadingStatistics = false;
            this.errorStatistics = null;
            this.startDate = null;
            this.endDate = null;
            this.selectedSubjects = {};

        },
        async onFormSubmit(event) {

            try {
                this.loadingStatistics = true
                this.errorStatistics = null

                const parameters = this.paramsProcessing(this.selectedSubjects, this.startDate, this.endDate)
                await this.updateStatisticsAPI(parameters)
            } catch (e) {
                this.errorStatistics = e.message
                this.dropStatistics()
                this.$emit('loadingError')
            } finally {
                this.loadingStatistics = false
                this.$emit('loadingSuccessful')
                this.setDefaultValue()
            }

        },

        selectModelUpdate(id, data) {
            // Reflect.set(this.selectedSubjects, 'id', data)
            this.selectedSubjects[id] = data
        },
        startDateModelUpdate(data) {
            this.startDate = data

        },
        endDateModelUpdate(data) {
            this.endDate = data
        },
        comboBoxModelUpdate(data) {

            const currentDate = new Date();
            const currentMonth = currentDate.getMonth();
            const currentYear = currentDate.getFullYear();

            if (data === "За прошлый месяц") {
                const startDate = new Date(currentYear, currentMonth - 1, 1);
                const endDate = new Date(currentYear, currentMonth, 0);

                this.startDate = this.dateFormat(startDate)
                this.endDate = this.dateFormat(endDate);

            } else if (data === "За прошлый квартал") {

                const currentQuarter = Math.floor(currentMonth / 3) + 1;
                const previousQuarter = currentQuarter - 1;
                const previousYear = currentYear - (previousQuarter === 0 ? 1 : 0);
                const startOfPreviousQuarter = new Date(previousYear, (previousQuarter - 1) * 3, 1);
                const endOfPreviousQuarter = new Date(previousYear, previousQuarter * 3, 0);

                this.startDate = this.dateFormat(startOfPreviousQuarter)
                this.endDate = this.dateFormat(endOfPreviousQuarter)

            } else if (data === "За прошлый год") {

                const startDate = new Date(currentYear - 1, 0, 1);
                const endDate = new Date(currentYear, 11, 31);

                this.startDate = this.dateFormat(startDate)
                this.endDate = this.dateFormat(endDate)
            }
        }
    },
    mounted() { },
}
</script>