<template>
    <v-select density="comfortable" clearable multiple variant="outlined" v-model="selectedItems" :label="name"
        :items="items">
        <template v-slot:selection="{ item, index }">
            <v-chip v-if="index < 1">
                <span>{{ item.title }}</span>
            </v-chip>
            <span v-if="index === 1" class="text-grey text-caption align-self-center">
                (+{{ selectedItems.length - 1 }} другие)
            </span>
        </template>
    </v-select>
</template>

<script>
export default {
    name: 'request-select',
    props: {
        name: { type: String, required: true },
        items: { type: Array, required: true },
    },
    data() {
        return {
            selectedItems: [],
        }
    },

}
</script>

<style scoped></style>
