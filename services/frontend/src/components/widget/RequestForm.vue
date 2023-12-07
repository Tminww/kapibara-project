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
            if (data === "За прошлый месяц") {
                // Получение текущей даты
                const currentDate = new Date();

                // Получение месяца и года текущей даты
                const currentMonth = currentDate.getMonth();
                const currentYear = currentDate.getFullYear();

                // Определение начальной даты прошлого месяца
                const startDate = new Date(currentYear, currentMonth - 1, 1);

                // Определение конечной даты прошлого месяца
                const endDate = new Date(currentYear, currentMonth, 0);

                // Преобразование дат в строковый формат
                const startDateString = startDate.toISOString().split('T')[0];
                const endDateString = endDate.toISOString().split('T')[0];

                // Вывод результатов
                console.log("Интервал дат прошлого месяца:");
                console.log("Начальная дата: " + startDateString);
                console.log("Конечная дата: " + endDateString);
                this.startDate = startDateString;
                this.endDate = endDateString;
            } else if (data === "За прошлый квартал") {
                // Получение текущей даты
                const currentDate = new Date();

                // Получение года и месяца текущей даты
                const currentYear = currentDate.getFullYear();
                const currentMonth = currentDate.getMonth();

                // Определение номера квартала текущей даты
                const currentQuarter = Math.floor((currentMonth + 3) / 3);

                // Определение начальной даты прошлого квартала
                const startMonth = (currentQuarter - 2) * 3 - 1;
                const startYear = currentQuarter === 1 ? currentYear - 1 : currentYear;
                const startDate = new Date(startYear, startMonth, 1);

                // Определение конечной даты прошлого квартала
                const endMonth = currentQuarter * 3 - 1;
                const endYear = currentYear;
                const endDate = new Date(endYear, endMonth + 1, 0);

                // Преобразование дат в строковый формат
                const startDateString = startDate.toISOString().split('T')[0];
                const endDateString = endDate.toISOString().split('T')[0];

                // Вывод результатов
                console.log("Интервал дат прошлого квартала:");
                console.log("Начальная дата: " + startDateString);
                console.log("Конечная дата: " + endDateString);

                this.startDate = startDateString;
                this.endDate = endDateString;

            } else if (data === "За прошлый год") {
                // Получение текущей даты
                const currentDate = new Date();

                // Получение года текущей даты
                const currentYear = currentDate.getFullYear();

                // Определение начальной даты прошлого года
                const startYear = currentYear - 1;
                const startDate = new Date(startYear, 0, 1);

                // Определение конечной даты прошлого года
                const endYear = startYear;
                const endDate = new Date(endYear, 11, 31);

                // Преобразование дат в строковый формат
                const startDateString = startDate.toISOString().split('T')[0];
                const endDateString = endDate.toISOString().split('T')[0];

                // Вывод результатов
                console.log("Интервал дат прошлого года:");
                console.log("Начальная дата: " + startDateString);
                console.log("Конечная дата: " + endDateString);

                this.startDate = startDateString;
                this.endDate = endDateString;
            }

        }
    },
    mounted() { },
}
</script>