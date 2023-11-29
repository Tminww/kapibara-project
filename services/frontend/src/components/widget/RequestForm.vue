<template>
    <div v-for="district in districts">
        <request-select :key="district.id" :name="district.name" :items="getRegionsName(district)" />
    </div>

    <v-divider class="mx-3" dark></v-divider>

    <v-combobox clearable density="comfortable" label="Выбор периода"
        :items="['За прошлую неделю', 'За прошлый месяц', 'За прошлый квартал', 'За прошлый год']"
        variant="outlined"></v-combobox>

    <date-picker label="Datepicker" v-model="date">
    </date-picker>
</template>

<script lang="js">
import RequestSelect from './RequestSelect.vue'
import DatePicker from './DatePicker.vue'
export default {
    name: 'request-form',
    components: { RequestSelect, DatePicker },
    props: {
        districts: { type: Object, required: true },
    },
    data() {
        return {
            items: [],
            date: null,

        }
    },
    methods: {
        getRegionsName(district) {
            let regionsName = []
            for (const region of district.regions) {
                regionsName.push(region.name)
            }
            console.log(regionsName)
            return regionsName
        },
    },
    mounted() { },
}
</script>
