<template>
    <v-form @submit.prevent="onFormSubmit()">
        <div v-for="district in districts" :key="district.id">
            <v-select density="comfortable" clearable multiple variant="outlined"
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
        <v-divider class="mx-3" dark></v-divider>

        <v-combobox clearable density="comfortable" label="Выбор периода" :items="[
            'За прошлую неделю',
            'За прошлый месяц',
            'За прошлый квартал',
            'За прошлый год',
        ]" variant="outlined"></v-combobox>

        <!-- <date-picker label="Datepicker" v-model="date"> </date-picker> -->
        <v-row>

            <v-col>
                <v-text-field @update:modelValue="e => startDateModelUpdate(e)" density="default" variant="solo"
                    type="date" />

            </v-col>
            <v-col>
                <v-text-field @update:modelValue="e => endDateModelUpdate(e)" density="default" variant="solo"
                    type="date" />

            </v-col>

        </v-row>
        <v-btn type="submit" :loading="loadingStatistics" text="Применить" />

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
        ...mapActions(['updateStatisticsAPI']),
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
            if (selected.length != 0) {
                const subjects = [];
                for (const subjectsInDistrict of Object.values(selected)) {
                    for (const subjectId of subjectsInDistrict) {
                        subjects.push(subjectId)
                    }
                }

                params["regions"] = subjects.toString();
            }
            return params

        },
        async onFormSubmit(event) {

            try {
                this.loadingStatistics = true
                this.errorStatistics = null
                console.log("submit_click")

                const parameters = this.paramsProcessing(this.selectedSubjects, this.startDate, this.endDate)
                console.log(parameters)
                await this.updateStatisticsAPI(parameters)
            } catch (e) {
                this.errorStatistics = e.message
            } finally {
                this.loadingStatistics = false
                console.log(this.getStatistics)
            }

        },
        selectModelUpdate(id, data) {
            // Reflect.set(this.selectedSubjects, 'id', data)
            this.selectedSubjects[id] = data
            console.log("Selected", this.selectedSubjects)
        },
        startDateModelUpdate(data) {
            this.startDate = data
            console.log("startDate", this.startDate)

        },
        endDateModelUpdate(data) {
            this.endDate = data
            console.log("endDate", this.endDate)
        },
    },
    mounted() { },
}
</script>