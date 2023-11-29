<template>
    <v-card class="rounded-xl mx-auto" elevation="0" variant="tonal" width="400">
        <v-card-title class="text-h6 mb-1">
            {{ name }}
        </v-card-title>

        <v-card-subtitle class="text-subtitle-2">
            {{ count }}
        </v-card-subtitle>

        <v-img src="./src/assets/pie.jpg" height="200px"> </v-img>

        <v-card-actions>
            <v-btn color="indigo" @click="visible = !visible">
                <template v-if="visible == true"> Закрыть Статистику </template>
                <template v-else> Открыть статистику </template>
            </v-btn>
        </v-card-actions>

        <!-- <v-card-text v-show="visible">

            <stat-base :stat="stat" />

        </v-card-text> -->

    </v-card>
</template>

<script lang="js">

export default {
    name: 'stat-region-card',
    components: {},
    props: {
        region: { type: Object, required: true },
    },
    data() {
        return {
            visible: false,
            name: this.region.name,
            count: this.region.count,
            stat: this.region.stat
        }
    },
}
</script>

<style scoped></style>
