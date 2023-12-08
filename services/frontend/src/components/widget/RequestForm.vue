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

        <v-combobox @update:modelValue="e => comboBoxModelUpdate(e)" clearable density="comfortable" label="Выбор периода"
            :items="[
                // 'За прошлую неделю',
                'За прошлый месяц',
                'За прошлый квартал',
                'За прошлый год',
            ]" variant="outlined"></v-combobox>

        <!-- <date-picker label="Datepicker" v-model="date"> </date-picker> -->
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
        <v-btn type=" submit" :loading="loadingStatistics" text="Применить" />

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
        async onFormSubmit(event) {

            try {
                this.loadingStatistics = true
                this.errorStatistics = null
                console.log("submit_click")

                const parameters = this.paramsProcessing(this.selectedSubjects, this.startDate, this.endDate)
                console.log("PARAMS", parameters)
                await this.updateStatisticsAPI(parameters)
            } catch (e) {
                this.errorStatistics = e.message
            } finally {
                this.loadingStatistics = false
                // this.selectedSubjects = {};
                // this.startDate = null;
                // this.endDate = null;
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
        comboBoxModelUpdate(data) {
            console.log("COMBOBOX", data)

            const currentDate = new Date();
            const currentMonth = currentDate.getMonth();
            const currentYear = currentDate.getFullYear();

            if (data === "За прошлый месяц") {
                const startDate = new Date(currentYear, currentMonth - 1, 1);
                const endDate = new Date(currentYear, currentMonth, 0);

                this.startDate = this.dateFormat(startDate)
                this.endDate = this.dateFormat(endDate);

            } else if (data === "За прошлый квартал") {
                switch (currentYear % 3) {
                    case 2:
                        {
                            const startDate = new Date(currentYear, currentMonth - 3, 1);
                            const endDate = new Date(currentYear, currentMonth, 0);

                            this.startDate = this.dateFormat(startDate)
                            this.endDate = this.dateFormat(endDate)
                            break;
                        }

                    case 1:
                        {
                            const startDate = new Date(currentYear, currentMonth - 6, 1);
                            const endDate = new Date(currentYear, currentMonth - 3, 0);

                            this.startDate = this.dateFormat(startDate)
                            this.endDate = this.dateFormat(endDate)
                            break;
                        }
                    case 0:
                        {
                            const startDate = new Date(currentYear, currentMonth - 6, 1);
                            const endDate = new Date(currentYear, currentMonth - 3, 0);

                            this.startDate = this.dateFormat(startDate)
                            this.endDate = this.dateFormat(endDate)
                            break;
                        }


                    default:
                        break;
                }


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