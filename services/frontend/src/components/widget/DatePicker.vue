<template>
    <v-menu v-model="showDatePicker" min-width="auto">
        <template v-slot:activator="{ on, attrs }">
            <v-text-field :label="label" :value="content" :rules="rules" :placeholder="placeholder"
                @click:clear="content = null" v-on="on" v-bind="attrs" prepend-inner-icon="mdi-calendar-blank-outline"
                clearable>
            </v-text-field>
        </template>
        <v-date-picker v-model="content" @change="showDatePicker = false"></v-date-picker>
    </v-menu>
</template>
  
<script>
export default {
    name: "date-picker",
    props: {
        value: {
            required: true,
        },
        label: {
            type: String,
            required: true,
        },
        placeholder: {
            type: String,
            default: 'YYYY-MM-DD',
        },
        rules: {
            type: Array,
            default: () => [],
        },
        required: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            showDatePicker: false,
        };
    },
    computed: {
        content: {
            get() {
                return this.value;
            },
            set(val) {
                this.$emit('input', val);
            },
        },
    },
};
</script>