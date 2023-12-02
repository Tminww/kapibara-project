<template>
    <v-form @submit.prevent>
        <div v-for="district in districts" :key="district.id">
            <v-select density="comfortable" clearable multiple variant="outlined"
                @update:modelValue="e => modelUpdate(district.id, e)" :label="district.name" item-title="name"
                item-value="id" :items="getRegionsName(district)">
                <template v-slot:selection="{ item, index }">
                    <div v-if="index < 1">
                        <span>{{ item.title }}</span>
                    </div>
                    <span v-if="index === 1" class="text-grey text-caption align-self-center">
                        (+{{ selectedRegions[district.id].length - 1 }} другие)
                    </span>
                </template>
            </v-select>
            <!-- <request-select
                :key="district.id"
                :name="district.name"
                :items="getRegionsName(district)"
            /> -->
        </div>
        <v-divider class="mx-3" dark></v-divider>

        <v-combobox clearable density="comfortable" label="Выбор периода" :items="[
            'За прошлую неделю',
            'За прошлый месяц',
            'За прошлый квартал',
            'За прошлый год',
        ]" variant="outlined"></v-combobox>

        <date-picker label="Datepicker" v-model="date"> </date-picker>
        <v-btn type="submit"> Применить </v-btn>
    </v-form>
</template>

<script lang="js">
// import RequestSelect from './RequestSelect.vue'
import DatePicker from './DatePicker.vue'
export default {
    name: 'request-form',
    components: { DatePicker },
    props: {
        districts: { type: Object, required: true },
    },
    data() {
        return {
            items: [],
            selectedRegions: {},
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
        onFormSubmit(e) {
            console.log(e.target.elements)
        },
        modelUpdate(id, data) {
            // Reflect.set(this.selectedRegions, 'id', data)
            this.selectedRegions[id] = data
            console.log(this.selectedRegions)
        },
    },
    mounted() { },
}
</script>